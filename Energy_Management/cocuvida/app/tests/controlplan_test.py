from cocuvida.controlplan.controlplanparser import ControlplanParser
from cocuvida.sqldatabase import stateschedule

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
    with open('tests/test_data/example_controlplan.yaml') as controlplan_file:
        res = await stateschedule.delete_states_for_plan_name_and_date(PLAN_NAME, OPERATION_DATE)
        self.assertTrue(res == 'delete')

        cp = ControlplanParser(controlplan_file.read())

        res = await cp.date_is_operating_date(OPERATION_DATE)
        self.assertTrue(res)

        res = await cp.generate_states(OPERATION_DATE)
        for i,row in enumerate(res):
            self.assertTrue(GENERATED_STATES[i] == row)

        res = await stateschedule.insert_states_from_generator(res)
        self.assertTrue(res == 'insert')

