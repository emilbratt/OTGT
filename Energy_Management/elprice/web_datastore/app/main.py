import os
from io import BytesIO

from typing import Optional
from fastapi import FastAPI, File, Request, status
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse, Response

POST_TEST_RESPONSE = 'test OK'

class TestModel(BaseModel):
    # identify caller (android device, browser, hostname etc.)
    caller: str

app = FastAPI()

@app.get("/test/get")
def test_get():
    return {'hello': 'world', 'test': 'OK'}

@app.post("/test/post")
def test_post(item: TestModel):
    return {item.caller: POST_TEST_RESPONSE}
