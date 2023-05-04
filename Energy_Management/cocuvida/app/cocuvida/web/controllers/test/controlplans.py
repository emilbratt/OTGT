from cocuvida.sqldatabase import (
    controlplans as sql_controlplans,
    stateschedule as sql_state_schedule
)

from .const import (
    BUTTON_TEST_SITE_CONTROLPLAN_PLAN_NAME,
    TEST_DATES
)

async def results(view: object, query_string: dict):
    await view.buttons(BUTTON_TEST_SITE_CONTROLPLAN_PLAN_NAME)
    if 'plan_name' not in query_string.keys():
        return view

    plan_name = query_string.get('plan_name')[0]
    all_rows = []
    for isodate in TEST_DATES:
        rows = await sql_state_schedule.select_all_states_for_date_and_plan_name(isodate, plan_name)
        for row in rows:
            all_rows.append(row)
    await view.show_state_schedule(all_rows)
    return view
