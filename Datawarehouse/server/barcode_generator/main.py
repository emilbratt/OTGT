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

import qrcode

from PIL import Image, ImageDraw, ImageFont

ENVIRONMENT_FILE = '../../environment.ini'
POST_TEST_RESPONSE = 'test OK'
SHEET_BARCODE_MAX_LIMIT = 36 # max barcodes that fit on a paper sheet
SHELF_LABEL_MAX_CHAR = 6 # max characters that fit on a shelf label
APP_DIR = os.path.dirname(os.path.realpath(__file__))
FONT = ImageFont.truetype(os.path.join(APP_DIR, 'font', 'FreeSans.ttf'), 72)
QRMODES = {
    'alphanumeric': 'REVOLUTION NO. 9', # chars, numbers and symbols (good for URL`s)
    'numeric': '64', # fastest but only positive numbers
}
if not os.path.isfile(ENVIRONMENT_FILE):
    exit('could not locate environment.ini, current path is set: ' + ENVIRONMENT_FILE)
config = configparser.ConfigParser()
config.sections()
config.read(ENVIRONMENT_FILE)


class TestModel(BaseModel):
    # identify caller (android device, browser, hostname etc.)
    caller: str


# barcodes and qr codes are generated based data in this model
class DataCodeModel(BaseModel):
    # barcode values go here
    barcodes: list
    # identify caller (android device, browser, hostname etc.)
    caller: str


class BarcodeGenerate:
    def __init__(self, barcodes = ['barcode']):
        self.barcodes = barcodes
        self.barcode_pixel_height = 90 # barcode height in pixels for sheet
        self.success = True
        self.label = 'nolabel'
        self.generated = {}
        self.msg = 'OK'


    def get_barcode_byte_array(self):
        rendered_barcode = self.barcode_obj.render()
        byte_array = io.BytesIO()
        rendered_barcode.save(byte_array, format='png')
        rendered_barcode.close()
        return byte_array.getvalue()

    def get_sheet_byte_array(self):
        byte_array = io.BytesIO()
        self.sheet_obj.save(byte_array, format='png')
        return byte_array.getvalue()

    def generate_single_barcode(self):
        self.label = self.barcodes[0]
        self.barcode_obj = Code128(self.label, writer=ImageWriter())

    def generate_shelf_label_sheet(self):
        # this is where we generate shelf labels for the inventory
        # which can be printed directly on paper sheet
        # with for example a vanilla hp printer

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

            # generate stock barcode
            self.barcode_obj = Code128(self.label, writer=ImageWriter())
            rendered_barcode = self.barcode_obj.render()

            # open a new blank for cropped barcode
            cropped_version = Image.new('RGB', (560,80), (255, 255, 255))

            # generate human readable text for barcode and paste into cropped blank
            human_label = ImageDraw.Draw(cropped_version)
            human_label.text((0,0), self.label, font=FONT, fill=(0, 0, 0))

            # crop out and paste barcode into cropped blank
            crop_dimension = (0, 80, rendered_barcode.size[0], 160)
            cropped_barcode = rendered_barcode.crop(crop_dimension)
            cropped_version.paste(cropped_barcode, (250,0))

            # paste cropped version into sheet
            self.sheet_obj.paste(cropped_version, (pixels_from_left,pixels_from_top))

            self.generated[self.label] = 'OK'
            rendered_barcode.close()
            cropped_version.close()

    def close_sheet(self):
        self.sheet_obj.close()


class BarcodeGenerateSingle(BarcodeGenerate):
    def __init__(self, barcode = 'barcode'):
        BarcodeGenerate.__init__(self, [barcode])
        self.generate_single_barcode()


class BarcodeGenerateShelfSingleSheet(BarcodeGenerate):
    def __init__(self, barcodes = ['barcode']):
        BarcodeGenerate.__init__(self, barcodes)
        # check max barcode count to make sure all fits on one sheet
        barcode_count = len(self.barcodes)
        if barcode_count > SHEET_BARCODE_MAX_LIMIT:
            self.success = False
            self.msg = 'max allowed barcodes: ' + str(SHEET_BARCODE_MAX_LIMIT) + ', barcodes sent: ' + str(barcode_count)
        self.generate_shelf_label_sheet()


class QRGenerate:
    def __init__(self, qrcodes = ['code']):
        self.qr_object = qrcode.QRCode(version=1,
                                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                                    box_size=10,
                                    border=2,)
        self.qrcode = qrcodes
        self.success = True
        self.label = 'nolabel'
        self.generated = {}
        self.msg = 'OK'

    def get_qrcode_byte_array(self):
        byte_array = io.BytesIO()
        rendered_qrcode = self.qr_object.make_image(fill_color="black", back_color="white")
        rendered_qrcode.save(byte_array, format='png')
        rendered_qrcode.close()
        return byte_array.getvalue()

    def generate_single_qrcode(self):
        self.label = self.qrcode[0]
        self.qr_object.add_data(self.label)
        self.qr_object.make(fit=True)



class QRGenerateSingle(QRGenerate):
    def __init__(self, barcode = 'barcode'):
        QRGenerate.__init__(self, [barcode])
        self.generate_single_qrcode()


app = FastAPI()


@app.get("/test/get")
def test_get():
    return {'hello': 'world', 'test': 'OK'}

@app.post("/test/post")
def test_post(item: TestModel):
    return {item.caller: POST_TEST_RESPONSE}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/cwd")
def read_cwd():
    return {"cwd": APP_DIR}

@app.get("/barcode/{barcode}")
async def barcode_single(barcode: str):
    b = BarcodeGenerateSingle(barcode)
    byte_array = b.get_barcode_byte_array()
    return Response(status_code=status.HTTP_201_CREATED,
                    content=byte_array, media_type="image/png")

@app.post("/barcode/single/")
async def barcode_single(item: DataCodeModel):
    b = BarcodeGenerateSingle(item.barcodes[0])
    byte_array = b.get_barcode_byte_array()
    return Response(status_code=status.HTTP_201_CREATED,
                    content=byte_array, media_type="image/png")

@app.get("/shelf/char/limit")
def shelf_char_limit():
    return {"limit": SHELF_LABEL_MAX_CHAR}

@app.get("/shelf/sheet/limit")
def sheet_limit():
    return {"limit": SHEET_BARCODE_MAX_LIMIT}

# using GET we can create one single barcode
@app.get("/shelf/{barcode}")
async def shelf_single(barcode: str):
    b = BarcodeGenerateShelfSingleSheet([barcode])
    byte_array = b.get_sheet_byte_array()
    b.close_sheet()
    return Response(status_code=status.HTTP_201_CREATED,
                    content=byte_array, media_type="image/png")

# using POST we can send an array with barcodes (max N that can fit on A4 sheet)
@app.post("/shelf/")
async def shelf_multiple(item: DataCodeModel):
    b = BarcodeGenerateShelfSingleSheet(item.barcodes)
    byte_array = b.get_sheet_byte_array()
    b.close_sheet()
    if b.success:
        return Response(status_code=status.HTTP_201_CREATED,
                        content=byte_array, media_type="image/png")
    else:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'response': b.msg})


@app.post("/qrcode/single/")
async def qrcode_single(item: DataCodeModel):
    b = QRGenerateSingle(item.barcodes[0])
    byte_array = b.get_qrcode_byte_array()
    return Response(status_code=status.HTTP_201_CREATED,
                    content=byte_array, media_type="image/png")
