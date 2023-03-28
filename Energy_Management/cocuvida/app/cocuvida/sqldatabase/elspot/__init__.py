import json

from cocuvida.sqldatabase import connect, select_one, select_all_no_param, insert_one, update, delete
from cocuvida.timehandle import isodates


async def list_elspot_regions() -> list:
    query = 'SELECT DISTINCT elspot_region FROM elspot_processed ORDER BY elspot_region'
    res = select_all_no_param(query)
    if res == None:
        return []
    res = [r[0] for r in res]
    return res

async def select_region_elspot_data_for_date_window(region: str, time_from: str, time_to: str):
    pass

async def select_region_elspot_data_for_date(region: str, isodate: str) -> list:
    query = '''
        SELECT elspot_data
        FROM elspot_processed
        WHERE elspot_region = ? AND elspot_date = ?
    '''
    res = select_one(query, [region, isodate])
    if res == None:
        return []
    return json.loads(res[0])

async def insert_raw_elspot(json_string: str) -> bool:
    '''
        only pass the raw data, the date is extracted from it
    '''
    insert_query = '''
        INSERT INTO elspot_raw
            (elspot_data, elspot_date)
        VALUES
            (?, ?)
    '''
    update_query = '''
        UPDATE elspot_raw
        SET elspot_data = ?
        WHERE elspot_date = ?
    '''
    time_stamp = json.loads(json_string)['data']['DataStartdate']
    time_stamp = isodates.date_object_from_isodate_and_time(time_stamp)
    elspot_date = time_stamp.date()
    res = insert_one(insert_query, [json_string, elspot_date])
    if res == 'insert':
        return True
    if res == 'IntegrityError':
        res = update(update_query, [json_string, elspot_date])
        if res == 'update':
            return True
    return False

async def elspot_raw_exists_for_date(isodate: str) -> bool:
    query = '''
        SELECT COUNT(elspot_data)
        FROM elspot_raw
        WHERE elspot_date = ?
    '''
    res = select_one(query, [isodate])
    return (res[0] == 1)

async def insert_processed_elspot(elspot_data: dict) -> bool:
    '''
        pass dict in this format
        {
            'region': 'Molde,
            'currency': 'NOK',
            'date':    'YYYY-MM-DD',
            'unit':    'ore/kWh',
            'max':     '280',
            'min':     '143',
            'average': '197',
            'resolution': 96, # (92 for 23 hours, 100 for 25 hours)
            'prices': [
                {'index': 0, 'time_start': '00:00', 'time_end': '00:15', 'value': '210'},
                {'index': 1, 'time_start': '00:15', 'time_end': '00:30', 'value': '210'},
                ..,
                {'index': 95, 'time_start': '23:45', 'time_end': '00:00', 'value': '247'}
            ]
        },
    '''
    insert_query = '''
        INSERT INTO elspot_processed
            (elspot_data, elspot_date, elspot_region)
        VALUES
            (?, ?, ?)
    '''
    update_query = '''
        UPDATE elspot_processed
        SET elspot_data = ?
        WHERE elspot_date = ? AND elspot_region = ?
    '''
    elspot_region = elspot_data['region']
    elspot_date = elspot_data['date']
    elspot_data = json.dumps(elspot_data)
    res = insert_one(insert_query, [elspot_data, elspot_date, elspot_region])
    if res == 'insert':
        return True
    if res == 'IntegrityError':
        res = update(update_query, [elspot_data, elspot_date, elspot_region])
        if res == 'update':
            return True
    return False

async def insert_plot_date(data: dict) -> bool:
    insert_query = '''
        INSERT INTO elspot_plot_date
            (plot_data, last_updated, plot_date, plot_region)
        VALUES
            (?, ?, ?, ?)
    '''
    update_query = '''
        UPDATE elspot_plot_date
        SET plot_data = ?, last_updated = ?
        WHERE plot_date = ? AND plot_region = ?
    '''

    plot_data = data['plot']
    last_updated = isodates.timestamp_now_round('second')
    plot_date = data['date']
    plot_region = data['region']

    res = insert_one(insert_query, [plot_data, last_updated, plot_date, plot_region])
    if res == 'insert':
        return True
    if res == 'IntegrityError':
        res = update(update_query, [plot_data, last_updated, plot_date, plot_region])
        if res == 'update':
            return True
    return False
