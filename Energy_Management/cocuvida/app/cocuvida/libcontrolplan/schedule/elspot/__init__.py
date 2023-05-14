from cocuvida.environment import env_ini_get
from cocuvida.sqldatabase import elspot as sql_elspot
from cocuvida.timehandle import isodates

from . import plans

REGION = env_ini_get(section='cocuvida', key='elspot_region')


async def generate_states(schedule_elspot_entry: dict, isodate: str) -> list:
    # NOT IMPLEMENTED, RETURNS BOGUS DATA FOR NOW
    elspot_data = await sql_elspot.select_processed_for_date_and_region(isodate, REGION)
    if elspot_data == {}:
        return []

    states = []
    for elspot_plan in schedule_elspot_entry:
        entrydata = schedule_elspot_entry[elspot_plan]
        for target, plan_options in entrydata.items():
            result = await plans.generate(elspot_plan, plan_options, elspot_data)
            if result == []:
                continue
            for row in result:
                state = row[0]
                timestamp = row[1]
                _row = [target, state, timestamp]
                # FIXME: handle 25 hour days
                if _row not in states:
                    # ..identical entry happens on a 25 hour day
                    # ..two entries with time 02:MM might be generated
                    states.append(_row)

    return states
