import asyncio
import yaml

from cocuvida.libcontrolplan import ControlPlan
from cocuvida.sqldatabase import (controlplans as sql_controlplans,
                                  stateschedule as sql_stateschedule)

PLAN_NAME = 'example_controlplan'
OPERATION_DATE = '2022-06-17'

# these should match the generated states from the controlplan in ./test_data/controlplan
CHECK_GENERATED_STATES = [
    ['example_controlplan', 'shelly', 'on', '2022-06-17 11:00', 2],
    ['example_controlplan', 'shelly', 'off', '2022-06-17 12:00', 2],
    ['example_controlplan', 'exampletarget', '60', '2022-06-17 12:00', 0],
    ['example_controlplan', 'mqtt', 'msgrefa', '2022-06-17 12:00', 2],
    ['example_controlplan', 'mqtt', 'msgrefb', '2022-06-17 13:00', 2],
    ['example_controlplan', 'shelly', 'toggle', '2022-06-17 17:30', 2],
]


def example_controlplan(self):
    with open('tests/test_data/controlplan/example_controlplan.yaml') as f:
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

        cp = ControlPlan()
        controlplan = yaml.safe_load(raw_content)
        asyncio.run(cp.load_controlplan(controlplan))

        # this should be an operating day
        res = asyncio.run(cp.is_operating_date(PLAN_NAME, OPERATION_DATE))
        self.assertTrue(res)

        # the generated states for the operation date should match the hardcoded ones
        generated_states = asyncio.run(cp.generate_states(PLAN_NAME, OPERATION_DATE))
        for row in generated_states:
            self.assertTrue(row in CHECK_GENERATED_STATES)

        # insert the generated states to DB
        res = asyncio.run(sql_stateschedule.insert_states_from_generator(generated_states))
        self.assertTrue(res == 'insert')

        # load states and publish
        res = asyncio.run(sql_stateschedule.select_non_published_states_for_timestamp('2022-06-17 12:00'))
        for row in res:
            plan_name = row[0]
            target_type = row[1]
            state_value = row[2]
            state_time = row[3]
            rowid = row[4]
            # only test if example target for now
            if target_type == 'exampletarget':
                res = asyncio.run(cp.publish_state(plan_name, target_type, state_value))
                if res:
                    # published -> 1
                    state_status = sql_stateschedule.STATUS_ENUMS.index('published')
                else:
                    # not publish -> 3
                    state_status = sql_stateschedule.STATUS_ENUMS.index['not published']
                # state_status should evaluates to 1 -> published
                self.assertTrue(state_status == 1)

                # update state_status to 1 -> published to DB
                res = asyncio.run(sql_stateschedule.update_state_status_by_rowid(rowid, state_status))
                self.assertTrue(res == 'update')
