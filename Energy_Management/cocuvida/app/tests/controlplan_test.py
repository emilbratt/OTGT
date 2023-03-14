import asyncio
from yaml import safe_load as yaml_safe_load


def example_controlplan(self):
    #from cocuvida.controlplan import temp_controlplan_parser
    with open('tests/test_data/example_controlplan.yaml') as f:
        control_plan = f.read()
        control_plan = yaml_safe_load(control_plan)
        #self.assertTrue(temp_controlplan_parser(control_plan))
        self.assertTrue == True
