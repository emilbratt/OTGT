import asyncio
import unittest

import yaml

from cocuvida.libcontrolplan import ControlPlan
from cocuvida.sqldatabase import (controlplans as sql_controlplans,
                                  stateschedule as sql_stateschedule)

FILES = {
    'example_controlplan': 'tests/test_data/controlplan/example_controlplan.yaml',
    'example_elspot': 'tests/test_data/controlplan/example_elspot.yaml',
}


# these should match the generated states from the controlplan in ./test_data/controlplan
def test_controlplan(self: unittest.TestCase, file_ref: str, operation_date: str):
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

        cp = ControlPlan()
        asyncio.run(cp.load_controlplan(controlplan))

        # this should be an operating day
        res = asyncio.run(cp.is_operating_date(plan_name, operation_date))
        self.assertTrue(res)

        # the generated states for the operation date should match the hardcoded ones
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
            target_included = asyncio.run(cp.target_is_included(plan_name, target_type))
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
