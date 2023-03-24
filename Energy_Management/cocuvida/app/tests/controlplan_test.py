import asyncio
import yaml

from cocuvida.controlplanparser import ControlplanParser
from cocuvida.sqldatabase import (controlplans as sql_controlplans,
                                  stateschedule as sql_stateschedule)

PLAN_NAME = 'example_controlplan'
OPERATION_DATE = '2023-06-17'
GENERATED_STATES = [
    ['example_controlplan', 'shelly', 'on', '2023-06-17 03:30', 0],
    ['example_controlplan', 'exampletarget', '60', '2023-06-17 12:00', 0],
    ['example_controlplan', 'mqtt', 'msgrefa', '2023-06-17 12:00', 0],
    ['example_controlplan', 'mqtt', 'msgrefb', '2023-06-17 13:00', 0],
    ['example_controlplan', 'shelly', 'off', '2023-06-17 17:30', 0],
]


def example_controlplan(self):
    with open('tests/test_data/example_controlplan.yaml') as f:
        raw_content = f.read()

        # if no records, still OK
        res = asyncio.run(sql_controlplans.delete_control_plan(PLAN_NAME))
        self.assertTrue(res == 'delete')

        # if no records, still OK
        res = asyncio.run(sql_stateschedule.delete_states_for_plan_name_and_date(PLAN_NAME, OPERATION_DATE))
        self.assertTrue(res == 'delete')

        # insert control plan
        res = asyncio.run(sql_controlplans.insert_control_plan(raw_content))
        self.assertTrue(res == 'insert')

        cp = ControlplanParser()
        controlplan = yaml.safe_load(raw_content)
        asyncio.run(cp.load_controlplan(controlplan))

        # this should be an operating day
        res = asyncio.run(cp.date_is_operating_date(PLAN_NAME, OPERATION_DATE))
        self.assertTrue(res)

        # the generated states for the operation date should match the hardcoded ones
        res = asyncio.run(cp.generate_states(PLAN_NAME, OPERATION_DATE))
        for i,row in enumerate(res):
            self.assertTrue(GENERATED_STATES[i] == row)

        # insert the generated states to DB
        res = asyncio.run(sql_stateschedule.insert_states_from_generator(res))
        self.assertTrue(res == 'insert')

        # load states and publish
        res = asyncio.run(sql_stateschedule.select_unpublished_for_timestamp('2023-06-17 12:00'))
        for row in res:
            plan_name = row[0]
            target_type = row[1]
            state_value = row[2]
            state_time = row[3]
            rowid = row[4]
            res = asyncio.run(cp.publish_state(plan_name, target_type, state_value))
            state_status = 1
            if not res:
                # publish failed
                state_status = 3
            self.assertTrue(state_status == 1)

            # update state_status to 1 -> published to DB
            res = asyncio.run(sql_stateschedule.update_state_status_by_rowid(rowid, state_status))
            self.assertTrue(res == 'update')
