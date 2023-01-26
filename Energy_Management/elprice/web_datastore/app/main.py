import os
from io import BytesIO

from typing import Optional
from fastapi import FastAPI, File, Request, status
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse, Response

from envars     import envar_get

POST_TEST_RESPONSE = 'test OK'

class TestModel(BaseModel):
    # identify caller (android device, browser, hostname etc.)
    caller: str

app = FastAPI()

@app.get("/test/get")
def test_get():
    return {'hello': 'world', 'test': 'OK'}

# getting ENVARS
@app.get('/envar/HOST_ALLOW_UPLOAD_ELSPOT')
def envar_HOST_ALLOW_UPLOAD_ELSPOT():
    return {'time today': envar_get('HOST_ALLOW_UPLOAD_ELSPOT')}

@app.get('/envar/HOST_ALLOW_UPLOAD_PLOT')
def envar_HOST_ALLOW_UPLOAD_PLOT():
    return {'time today': envar_get('HOST_ALLOW_UPLOAD_PLOT')}

@app.get('/envar/HOST_ALLOW_UPLOAD_SENSOR')
def envar_HOST_ALLOW_UPLOAD_SENSOR():
    return {'time today': envar_get('HOST_ALLOW_UPLOAD_SENSOR')}

@app.post("/test/post")
def test_post(item: TestModel):
    return {item.caller: POST_TEST_RESPONSE}
