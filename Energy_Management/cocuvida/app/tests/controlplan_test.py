import yaml

from cocuvida.controlplanparser import ControlplanParser
from cocuvida.sqldatabase import (controlplans as sql_controlplans,
                                  stateschedule as sql_stateschedule)

PLAN_NAME = 'example_controlplan'
OPERATION_DATE = '2023-06-17'
GENERATED_STATES = [
    ['example_controlplan', 'shelly', 'on', '2023-06-17 03:30'],
    ['example_controlplan', 'someintegration', '60', '2023-06-17 12:00'],
    ['example_controlplan', 'mqtt', 'msgrefa', '2023-06-17 12:00'],
    ['example_controlplan', 'mqtt', 'msgrefb', '2023-06-17 13:00'],
    ['example_controlplan', 'shelly', 'off', '2023-06-17 17:30'],
]


async def example_controlplan(self):
    with open('tests/test_data/example_controlplan.yaml') as f:
        raw_content = f.read()

        # if no records, still OK
        res = await sql_controlplans.delete_control_plan(PLAN_NAME)
        self.assertTrue(res == 'delete')

        # if no records, still OK
        res = await sql_stateschedule.delete_states_for_plan_name_and_date(PLAN_NAME, OPERATION_DATE)
        self.assertTrue(res == 'delete')

        # insert control plan
        res = await sql_controlplans.insert_control_plan(raw_content)
        self.assertTrue(res == 'insert')

        cp = ControlplanParser()
        await cp.load_controlplan(yaml.safe_load(raw_content))

        # this should be an operating day
        res = await cp.date_is_operating_date(OPERATION_DATE)
        self.assertTrue(res)

        # the generated states for the operation date should match the hardcoded ones
        res = await cp.generate_states(OPERATION_DATE)
        for i,row in enumerate(res):
            self.assertTrue(GENERATED_STATES[i] == row)

        # insert the generated states
        res = await sql_stateschedule.insert_states_from_generator(res)
        self.assertTrue(res == 'insert')

