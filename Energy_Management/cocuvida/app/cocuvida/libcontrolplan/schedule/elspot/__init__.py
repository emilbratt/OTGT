from cocuvida.environment import env_ini_get
from cocuvida.sqldatabase import elspot as sql_elspot
from cocuvida.timehandle import isodates

from . import plans

REGION = env_ini_get(section='cocuvida', key='elspot_region')


async def generate_states(schedule_elspot_entry: dict, isodate: str) -> list:
    # NOT IMPLEMENTED, RETURNS BOGUS DATA FOR NOW
    entries = []
    for name in schedule_elspot_entry:
        if name != 'include_entry':
            entries.append(name)
    if entries == []:
        return []

    elspot_data = await sql_elspot.select_processed_for_date_and_region(isodate, REGION)
    if elspot_data == {}:
        return []

    states = []
    for state_plan in entries:
        entrydata = schedule_elspot_entry[state_plan]
        for target, plan_options in entrydata.items():
            result = await plans.generate(state_plan, plan_options, elspot_data)
            if result == []:
                continue
            for row in result:
                state = row[0]
                timestamp = row[1]
                _row = [target, state, timestamp]
                if _row not in states:
                    # FIXME: handle 25 hour days
                    # ..identical entry happens on a 25 hour day
                    # ..two entries with time 02:MM might be generated
                    states.append(_row)

    return states
