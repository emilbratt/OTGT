
from yaml import safe_load as yaml_safe_load

from cocuvida.controlplan.controlplanparser import ControlplanParser
from cocuvida.sqldatabase.stateschedule import insert_states_from_generator


async def generate_controlplan_states(self):
    with open('tests/test_data/example_controlplan.yaml') as controlplan_file:
        some_included_date = '2023-06-17'

        cp = ControlplanParser(controlplan_file.read())

        res = await cp.date_is_operating_date(some_included_date)
        self.assertTrue(res)

        res = await cp.generate_states(some_included_date)
        for row in res:
            print(row)

        res = await insert_states_from_generator(res)
        print(res)
