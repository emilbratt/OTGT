from fastapi import FastAPI, File, Request, status, HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse, Response

### imports for the future if needed
# from typing import Optional
# from io import BytesIO
# from fastapi.staticfiles import StaticFiles

from envars import envar_get
from urldatamodel import datamodelelspot
from allowedhosts import HostFilter
from sqldatabase import sqldatabaseinit

app = FastAPI()

# testing
@app.get("/test/get")
def test_get():
    return {'hello': 'world', 'test': 'OK'}
@app.get("/test/get/{var}")
def test_get_var(var: str):
    print(var)
@app.get('/envar/HOST_ALLOW_UPLOAD_ELSPOT')
def envar_HOST_ALLOW_UPLOAD_ELSPOT():
    return {'HOST_ALLOW_UPLOAD_ELSPOT': envar_get('HOST_ALLOW_UPLOAD_ELSPOT')}
@app.get('/envar/HOST_ALLOW_UPLOAD_PLOT')
def envar_HOST_ALLOW_UPLOAD_PLOT():
    return {'HOST_ALLOW_UPLOAD_ELSPOT': envar_get('HOST_ALLOW_UPLOAD_PLOT')}
@app.get('/envar/HOST_ALLOW_UPLOAD_SENSOR')
def envar_HOST_ALLOW_UPLOAD_SENSOR():
    return {'HOST_ALLOW_UPLOAD_ELSPOT': envar_get('HOST_ALLOW_UPLOAD_SENSOR')}
@app.post("/show/param")
def show_params(request: Request):
    print(request.query_params["key"])


# elspot raw
@app.post('/elspot/raw', status_code=status.HTTP_201_CREATED)
def post_elspot_raw(request: Request, datamodel: datamodelelspot.Raw):
    allowed_host = HostFilter(envar_get)
    databasehandle = sqldatabaseinit(envar_get)
    # if not allowed_host.elspot(request.client.host):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    if not datamodel.check(envar_get):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid data')
    action = databasehandle.elspot().insert().raw_v1(datamodel)
    if action == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Data was not saved to database')
    else:
        return { 'date': datamodel.date, 'action': action }

@app.head('/elspot/raw/{the_date}', status_code=status.HTTP_200_OK)
def head_elspot_raw(the_date: str):
    res = sqldatabaseinit(envar_get).elspot().select().raw_exists_v1(the_date)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get('/elspot/raw/{the_date}', status_code=status.HTTP_200_OK)
def get_elspot_raw(the_date: str):
    res = sqldatabaseinit(envar_get).elspot().select().raw_v1(the_date)
    if res == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no data for date ' + the_date)
    else:
        return res


# elspot reshaped
@app.post('/elspot/reshaped', status_code=status.HTTP_201_CREATED)
def post_elspot_reshaped(request: Request, datamodel: datamodelelspot.Reshaped):
    allowed_host = HostFilter(envar_get)
    databasehandle = sqldatabaseinit(envar_get)
    # if not allowed_host.elspot(request.client.host):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    if not datamodel.check(envar_get):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid data')
    action = databasehandle.elspot().insert().reshaped_v1(datamodel)
    if action == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Data was not saved to database')
    return { 'region': datamodel.region, 'date': datamodel.date, 'action': action }

@app.head('/elspot/reshaped/{the_date}', status_code=status.HTTP_200_OK)
def head_elspot_reshaped(the_date: str):
    res = sqldatabaseinit(envar_get).elspot().select().reshaped_exists_v1(the_date)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get('/elspot/reshaped/{the_region}/{the_date}', status_code=status.HTTP_200_OK)
def get_elspot_reshaped(the_region: str, the_date: str):
    res = sqldatabaseinit(envar_get).elspot().select().reshaped_v1(the_region, the_date)
    if res == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no data for date ' + the_date)
    else:
        return res
