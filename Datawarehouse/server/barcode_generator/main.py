import sys
import requests
import configparser
import os

from typing import Optional
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from barcode import *


ENVIRONMENT_FILE = '../../environment.ini'

if not os.path.isfile(ENVIRONMENT_FILE):
    exit('could not locate environment.ini, current path is set: ' + ENVIRONMENT_FILE)

config = configparser.ConfigParser()
config.sections()
config.read(ENVIRONMENT_FILE)


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/cwd")
def read_root():
    MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
    return {"cwd": MAIN_DIR}

@app.get("/url")
def read_root():
    return {"cwd": config['datawarehouse']['datawarehouse_ip'].strip('"')}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    if item_id == 1:
        q = 'here is item 1'
    if item_id == 2:
        q = 'this is item 2'
    return {"item_id": item_id, "item": q}
