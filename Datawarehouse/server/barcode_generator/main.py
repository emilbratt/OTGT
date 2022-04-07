import sys
import requests
import configparser
import os
import io

from typing import Optional
from fastapi import FastAPI, Request, status
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, StreamingResponse, Response

from barcode.writer import ImageWriter
from barcode import Code128
from PIL import Image, ImageDraw, ImageFont

ENVIRONMENT_FILE = '../../environment.ini'
POST_TEST_RESPONSE = 'test OK'
APP_DIR = os.path.dirname(os.path.realpath(__file__))
FONT = ImageFont.truetype(os.path.join(APP_DIR, 'font', 'FreeSans.ttf'), 72)
BARCODE_DIR = os.path.join('/', 'barcodes')
SHEET_BARCODE_MAX_LIMIT = 36 # max barcodes that fit on a paper sheet
if not os.path.isdir(BARCODE_DIR):
    os.mkdir(BARCODE_DIR)
if not os.path.isfile(ENVIRONMENT_FILE):
    exit('could not locate environment.ini, current path is set: ' + ENVIRONMENT_FILE)
config = configparser.ConfigParser()
config.sections()
config.read(ENVIRONMENT_FILE)


class TestModel(BaseModel):
    # identify caller (android device, browser, hostname etc.)
    caller: str


class BarcodeModel(BaseModel):
    # barcode values go here
    barcodes: list
    # identify caller (android device, browser, hostname etc.)
    caller: str


class BarcodeGenerate:
    def __init__(self, barcodes = ['barcode']):
        self.barcodes = barcodes
        self.sheet_filename = os.path.join(BARCODE_DIR, 'final')
        self.barcode_pixel_height = 90 # barcode height in pixels for sheet
        self.success = True
        self.label = 'nolabel'
        self.generated = {}
        self.msg = 'OK'

    def barcode_to_byte_array(self):
        byte_array = io.BytesIO()
        self.barcode_obj.save(byte_array, format='png')
        byte_array = byte_array.getvalue()
        return byte_array

    def sheet_to_byte_array(self):
        byte_array = io.BytesIO()
        self.sheet_obj.save(byte_array, format='png')
        byte_array = byte_array.getvalue()
        return byte_array

    def generate_barcode(self):
        self.barcode_obj = Code128(self.label, writer=ImageWriter())

    def render_barcode(self):
        self.rendered_barcode = self.barcode_obj.render()

    def save_barcode(self):
        self.barcode_obj.save(self.barcode_path)

    def generate_shelf_label_sheet(self):
        # pixels from left where we paste into sheet
        pixels_from_left = 65
        self.sheet_obj = Image.new('RGB',(1240,1754), (255, 255, 255))
        self.sheet_obj.convert('L')
        for i,barcode in enumerate(self.barcodes):
            # half-way through we start pasting labels on right side of sheet
            if 1 + i > SHEET_BARCODE_MAX_LIMIT // 2:
                pixels_from_left = 645
            pixels_from_top = self.barcode_pixel_height * (i % (SHEET_BARCODE_MAX_LIMIT // 2)) + 75
            self.label = barcode
            self.barcode_path = os.path.join(BARCODE_DIR, self.label)

            # generate stock barcode
            self.barcode_obj = Code128(self.label, writer=ImageWriter())
            self.render_barcode()

            # open a new blank for cropped barcode
            cropped_version = Image.new('RGB', (560,80), (255, 255, 255))

            # generate human readable text for barcode and paste into cropped blank
            human_label = ImageDraw.Draw(cropped_version)
            human_label.text((0,0), self.label, font=FONT, fill=(0, 0, 0))

            # crop out and paste barcode into cropped blank
            crop_dimension = (0, 80, self.rendered_barcode.size[0], 160)
            cropped_barcode = self.rendered_barcode.crop(crop_dimension)
            cropped_version.paste(cropped_barcode, (250,0))

            # paste cropped version into sheet
            self.sheet_obj.paste(cropped_version, (pixels_from_left,pixels_from_top))

            self.generated[self.label] = 'OK'
            self.rendered_barcode.close()
            cropped_version.close()

    def save_sheet(self):
        self.sheet_obj.save('%s.png' % self.sheet_filename)

    def close_sheet(self):
        self.sheet_obj.close()


class BarcodeGenerateShelfSingleSheet(BarcodeGenerate):
    def __init__(self, barcodes = ['barcode']):
        BarcodeGenerate.__init__(self, barcodes)
        # check max barcode count to make sure all fits on one sheet
        barcode_count = len(self.barcodes)
        if barcode_count > SHEET_BARCODE_MAX_LIMIT:
            self.success = False
            self.msg = 'max allowed barcodes: ' + str(SHEET_BARCODE_MAX_LIMIT) + ', barcodes sent: ' + str(barcode_count)
        self.generate_shelf_label_sheet()


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/cwd")
def read_cwd():
    return {"cwd": APP_DIR}

@app.get("/shelf/sheet/limit")
def sheet_limit():
    return {"limit": SHEET_BARCODE_MAX_LIMIT}

@app.get("/test/get")
def test_get():
    return {'hello': 'world', 'test': 'OK'}

@app.post("/test/post")
def test_post(item: TestModel):
    return {item.caller: POST_TEST_RESPONSE}

# using GET we can create one single barcode
@app.get("/shelf/{barcode}")
async def shelf_single(barcode: str):
    b = BarcodeGenerateShelfSingleSheet([barcode])
    byte_array = b.sheet_to_byte_array()
    b.close_sheet()
    return Response(status_code=status.HTTP_201_CREATED,
                    content=byte_array, media_type="image/png")

# using POST we can send an array with barcodes (max N that can fit on A4 sheet)
@app.post("/shelf/")
async def shelf_multiple(item: BarcodeModel):
    b = BarcodeGenerateShelfSingleSheet(item.barcodes)
    byte_array = b.sheet_to_byte_array()
    b.close_sheet()
    if b.success:
        return Response(status_code=status.HTTP_201_CREATED,
                        content=byte_array, media_type="image/png")
    else:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'response': b.msg})

# using POST we can send an array with barcodes (max N that can fit on A4 sheet)
@app.post("/shelf/store/")
async def shelf_multiple(item: BarcodeModel):
    b = BarcodeGenerateShelfSingleSheet(item.barcodes)
    b.save_sheet()
    b.close_sheet()
    if b.success:
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"response": b.msg, 'generated': b.generated})
    else:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'response': b.msg})
