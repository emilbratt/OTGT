from cocuvida.environment import env_ini_get
from cocuvida.sqldatabase import elspot as sql_elspot
from cocuvida.timehandle import isodates

from .const import ENTRIES

from . import entries

REGION = env_ini_get(section='cocuvida', key='elspot_region')


async def generate_states(schedule_elspot_entry: dict, isodate: str) -> list:
    # NOT IMPLEMENTED, RETURNS BOGUS DATA FOR NOW
    res = await sql_elspot.select_processed_for_date_and_region(isodate, REGION)
    states = [
        ['exampletarget', '60', f'{isodate} 12:00'],
        ['exampletarget', '60', f'{isodate} 13:00'],
    ]
    return states
