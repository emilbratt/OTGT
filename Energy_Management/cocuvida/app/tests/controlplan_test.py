import asyncio
import unittest

import yaml

from cocuvida import libcontrolplan
from cocuvida.sqldatabase import controlplans as sql_controlplans
from cocuvida.sqldatabase import stateschedule as sql_stateschedule
from cocuvida.timehandle import isodates

FILES = {
    'example_time_schedule': 'tests/test_data/controlplan/example_time_schedule.yaml',
    'example_elspot_schedule': 'tests/test_data/controlplan/example_elspot_schedule.yaml',
}

TEST_UPLOADED_CONTROLPLAN_NAME = 'test_uploaded_controlplan'


# these should match the generated states from the controlplan in ./test_data/controlplan
def example_controlplan(self: unittest.TestCase, file_ref: str, operation_date: str):
    with open(FILES[file_ref]) as f:
        raw_content = f.read()
        controlplan = yaml.safe_load(raw_content)
        plan_name = controlplan['name']

        # if no records, still OK
        res = asyncio.run(sql_controlplans.delete_control_plan(plan_name))
        self.assertTrue(res == 'delete')

        # if no records, still OK
        res = asyncio.run(sql_stateschedule.delete_states_for_plan_name_and_date(plan_name, operation_date))
        self.assertTrue(res == 'delete')

        # insert control plan
        res = asyncio.run(sql_controlplans.insert_control_plan(raw_content))
        self.assertTrue(res == 'insert')

        cp = libcontrolplan.ControlPlan()
        asyncio.run(cp.load_controlplan(controlplan))

        # this should be an operating day
        res = asyncio.run(cp.is_operating_date(plan_name, operation_date))
        self.assertTrue(res)

        generated_states = asyncio.run(cp.generate_states(plan_name, operation_date))
        # insert the generated states to DB
        res = asyncio.run(sql_stateschedule.insert_states_from_generator(generated_states))
        self.assertTrue(res == 'insert')

        # load states and publish
        res = asyncio.run(sql_stateschedule.select_all_states_for_date_and_plan_name(operation_date, plan_name))
        for row in res:
            target_type = row[1]
            state_value = row[2]
            state_time = row[3]
            rowid = row[5]
            # only run "dummy" publish using exampletarget
            target_included = asyncio.run(cp.target_enabled(plan_name, target_type))
            if target_included:
                was_published = asyncio.run(cp.publish_state(plan_name, target_type, state_value))
                if was_published:
                    state_status = sql_stateschedule.STATUS_ENUMS.index('published')
                    self.assertTrue(state_status == 1)
                if not was_published:
                    state_status = sql_stateschedule.STATUS_ENUMS.index('publish failed')
                    self.assertTrue(state_status == 3)
            if not target_included:
                state_status = sql_stateschedule.STATUS_ENUMS.index('target disabled')
                self.assertTrue(state_status == 2)

            # update state_status to -> published to DB
            res = asyncio.run(sql_stateschedule.update_state_status_by_rowid(rowid, state_status))
            self.assertTrue(res == 'update')

def uploaded_controlplan(self):
    plan_name = TEST_UPLOADED_CONTROLPLAN_NAME
    plan_data = asyncio.run(sql_controlplans.select_control_plan_by_plan_name(plan_name))
    if plan_data == {}:
        return True

    from tests.libtest import targets
    cp = libcontrolplan.ControlPlan()
    asyncio.run(cp.load_controlplan(plan_data))
    res = asyncio.run(cp.is_operating_date(plan_name, isodates.today()))

    # generate and insert the generated states to DB
    generated_states = asyncio.run(cp.generate_states(plan_name, isodates.today()))
    res = asyncio.run(sql_stateschedule.insert_states_from_generator(generated_states))
    self.assertTrue(res == 'insert')

    # test publishing to targets found in controlplan
    for target_entry in plan_data['target']:
        match target_entry:
            case 'mqtt':
                asyncio.run(targets.mqtt.publish_state(plan_data['target'][target_entry]))
            case 'shelly':
                asyncio.run(targets.shelly.publish_state(plan_data['target'][target_entry]))
