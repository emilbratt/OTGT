import sys
import requests
import configparser
import os

from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

from barcode.writer import ImageWriter
from barcode import Code128
from PIL import Image, ImageDraw, ImageFont

APP_DIR = os.path.dirname(os.path.realpath(__file__))
BARCODE_DIR = os.path.join('/', 'barcode')
if not os.path.isdir(BARCODE_DIR):
    os.mkdir(BARCODE_DIR)

ENVIRONMENT_FILE = '../../environment.ini'

if not os.path.isfile(ENVIRONMENT_FILE):
    exit('could not locate environment.ini, current path is set: ' + ENVIRONMENT_FILE)

config = configparser.ConfigParser()
config.sections()
config.read(ENVIRONMENT_FILE)


class BarcodeModel(BaseModel):
    # barcode values go here
    barcodes: list
    # identify caller (android device, pc browser, script etc.)
    caller: str


class BarcodeGenerate:
    def __init__(self, barcodes = ['barcode']):
        self.barcodes = barcodes

    def generate(self):
        for barcode in self.barcodes:
            cur_file = os.path.join(BARCODE_DIR, barcode)
            Code128(barcode, writer=ImageWriter()).save(cur_file)


class BarcodeGenerateShelf(BarcodeGenerate):
    def __init__(self, barcodes = ['barcode']):
        BarcodeGenerate.__init__(self, barcodes)


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/cwd")
def read_root():
    return {"cwd": APP_DIR}

@app.get("/barcode_generate/shelf/single/{barcode}")
async def shelf_single(barcode: str):
    b = BarcodeGenerateShelf([barcode])
    b.generate()
    return {'Barcode': barcode}

@app.post("/barcode_generate/shelf/multiple/")
async def shelf_multiple(item: BarcodeModel):
    b = BarcodeGenerateShelf(item.barcodes)
    b.generate()
    return {"Called by": item.caller, "barcodes": item.barcodes}
