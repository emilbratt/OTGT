import json

from cocuvida.sqldatabase import connect, select_one, insert_one, update
from cocuvida.timehandle import isodates


async def insert_raw_elspot(json_string: str) -> str:
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

async def elspot_raw_exists_for_date(isodate: str):
    query = '''
        SELECT COUNT(elspot_data)
        FROM elspot_raw
        WHERE elspot_date = ?
    '''
    res = select_one(query, [isodate])
    return (res[0] == 1)
