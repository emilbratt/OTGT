from cocuvida.sqldatabase import (
    controlplans as sql_controlplans,
    stateschedule as sql_state_schedule
)

from .const import BUTTON_TEST_SITE_CONTROLPLAN_PLAN_NAME


async def results(view: object, query_string: dict):
    await view.buttons(BUTTON_TEST_SITE_CONTROLPLAN_PLAN_NAME)
    if 'plan_name' not in query_string.keys():
        return view

    plan_name = query_string.get('plan_name')[0]
    rows = await sql_state_schedule.select_states_today_for_plan_name(plan_name)
    await view.show_state_schedule(rows)
    return view
