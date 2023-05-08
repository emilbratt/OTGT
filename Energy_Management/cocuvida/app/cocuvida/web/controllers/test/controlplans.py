from cocuvida.libcontrolplan import ControlPlan
from cocuvida.sqldatabase import controlplans as sql_controlplans
from cocuvida.sqldatabase import stateschedule as sql_stateschedule
from cocuvida.timehandle import isodates

from .const import (
    BUTTON_TEST_SITE_CONTROLPLAN_PLAN_NAME,
    TEST_DATES
)



async def results(view: object, query_string: dict):
    await view.buttons(BUTTON_TEST_SITE_CONTROLPLAN_PLAN_NAME)
    if 'plan_name' not in query_string.keys():
        return view

    plan_name = query_string.get('plan_name')[0]
    plan_data = await sql_controlplans.select_control_plan_by_plan_name(plan_name)
    if plan_data == {}:
        return view

    cp = ControlPlan()
    date_today = isodates.today()
    await cp.load_controlplan(plan_data)
    operates_today = await cp.is_operating_date(plan_name, isodates.today())
    paragraph = f'Controlplan Calendar | Operates Today {date_today}: '
    if operates_today:
        paragraph += '<strong>yes</strong>'
    else:
        paragraph += '<strong>no</strong>'
    await view.add_paragraph(paragraph)

    # # this should be an operating day

    all_rows = []
    for isodate in TEST_DATES:
        rows = await sql_stateschedule.select_all_states_for_date_and_plan_name(isodate, plan_name)
        for row in rows:
            all_rows.append(row)
    await view.show_state_schedule(all_rows)
    return view
