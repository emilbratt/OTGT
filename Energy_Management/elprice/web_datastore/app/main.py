from fastapi import FastAPI, File, Request, status, HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse, Response
from envars       import envar_get
from urldatamodel import datamodelelspot, datamodelplot
from allowedhosts import HostFilter
from sqldatabase  import sqldatabasecrud, sqldatabaseschema
from mqttpublish  import mqttpublishinit


### init ###
# create database
db_schema = sqldatabaseschema(envar_get)
db_schema.create_database()
# load crud object
db_crud = sqldatabasecrud(envar_get)
# load mqtt publish object
mqtt_pub = mqttpublishinit(envar_get)
# load fastapi "app" object for the uvicorn ASGI web server implementation for Python
app = FastAPI()


### testing ###
@app.get('/test/get')
def test_get():
    return {'hello': 'world', 'test': 'OK'}
@app.get('/test/get/{var}')
def test_get_var(var: str):
    print(var)
@app.post('/show/param')
def show_params(request: Request):
    print(request.query_params['key'])
@app.get('/test/mqttpublish')
def test_get():
    return {'hello': 'world', 'test': 'OK'}


### developing ###

# manage database tables via browser using GET requests
@app.get('/dev/database/{table}/{operation}', status_code=status.HTTP_200_OK)
def dev_database(table: str, operation: str):
    return db_schema.manage(table=table, operation=operation)

### production ###

# elspot raw
@app.post('/elspot/raw/v0', status_code=status.HTTP_201_CREATED)
def post_elspot_raw_v0(request: Request, datamodel: datamodelelspot.Raw_v0):
    allowed_host = HostFilter(envar_get)
    # if not allowed_host.elspot(request.client.host):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    if not datamodel.check(envar_get):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid data')
    action = db_crud.elspot().insert().raw_v0(datamodel)
    if action == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Data was not saved to database')
    else:
        return { 'date': datamodel.date, 'action': action }

@app.head('/elspot/raw/v0/{the_date}', status_code=status.HTTP_200_OK)
def head_elspot_raw_v0(the_date: str):
    res = db_crud.elspot().select().raw_exists_v0(the_date)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get('/elspot/raw/v0/{the_date}', status_code=status.HTTP_200_OK)
def get_elspot_raw_v0(the_date: str):
    res = db_crud.elspot().select().raw_v0(the_date)
    if res == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no data for date ' + the_date)
    else:
        return res


# elspot reshaped
@app.post('/elspot/reshaped/v1', status_code=status.HTTP_201_CREATED)
def post_elspot_reshaped_v1(request: Request, datamodel: datamodelelspot.Reshaped_v1):
    allowed_host = HostFilter(envar_get)
    # if not allowed_host.elspot(request.client.host):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    if not datamodel.check(envar_get):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid data')
    action = db_crud.elspot().insert().reshaped_v1(datamodel)
    if action == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Data was not saved to database')
    else:
        topic = envar_get('MQTT_TOPIC_ELPRICE_ELSPOT_RESHAPED')
        mqtt_pub.single(topic=topic, payload=datamodel.get_json_data(), qos=1)
        return { 'date': datamodel.date, 'action': action }

@app.head('/elspot/reshaped/v1/{the_date}', status_code=status.HTTP_200_OK)
def head_elspot_reshaped_v1(the_date: str):
    res = db_crud.elspot().select().reshaped_exists_v1(the_date)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get('/elspot/reshaped/v1/{the_date}', status_code=status.HTTP_200_OK)
def get_elspot_reshaped_v1(the_date: str):
    res = db_crud.elspot().select().reshaped_v1(the_date)
    if res == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return res


# plots bydate
@app.post('/plot/bydate/v0', status_code=status.HTTP_201_CREATED)
def post_plot_bydate_v0(request: Request, datamodel: datamodelplot.ByDate_v0):
    allowed_host = HostFilter(envar_get)
    # if not allowed_host.elspot(request.client.host):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    action = db_crud.plot().insert().bydate_v0(datamodel)
    if action == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return { 'date': datamodel.date, 'region': datamodel.region, 'action': action }

@app.head('/plot/bydate/v0/{the_region}/{the_date}', status_code=status.HTTP_200_OK)
def head_plot_bydate_v0(the_region: str, the_date: str):
    res = db_crud.plot().select().bydate_v0(the_region, the_date)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get('/plot/bydate/v0/{the_region}/{the_date}', status_code=status.HTTP_200_OK)
def get_plot_bydate_v0(the_region: str, the_date: str):
    res = db_crud.plot().select().bydate_v0(the_region, the_date)
    if res == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(content=res, media_type='image/svg+xml')


# plots byhour
@app.post('/plot/byhour/v0', status_code=status.HTTP_201_CREATED)
def post_plot_byhour_v0(request: Request, datamodel: datamodelplot.ByHour_v0):
    allowed_host = HostFilter(envar_get)
    # if not allowed_host.elspot(request.client.host):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    action = db_crud.plot().insert().byhour_v0(datamodel)
    if action == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return { 'date': datamodel.date, 'region': datamodel.region, 'action': action }

@app.head('/plot/byhour/v0/{the_region}/{the_date}/{the_index}', status_code=status.HTTP_200_OK)
def head_plot_byhour_v0(the_region: str, the_date: str, the_index: str):
    res = db_crud.plot().select().byhour_v0(the_region, the_date, the_index)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get('/plot/byhour/v0/{the_region}/{the_date}/{the_index}', status_code=status.HTTP_200_OK)
def get_plot_byhour_v0(the_region: str, the_date: str, the_index: str):
    res = db_crud.plot().select().byhour_v0(the_region, the_date, the_index)
    if res == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(content=res, media_type='image/svg+xml')
