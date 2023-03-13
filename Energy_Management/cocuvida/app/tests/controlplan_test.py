from yaml import safe_load as yaml_safe_load

from cocuvida.controlplan import temp_controlplan_parser


def example_controlplan(self):
    with open('tests/test_data/example_controlplan.yaml') as f:
        control_plan = f.read()
        control_plan = yaml_safe_load(control_plan)
        self.assertTrue(temp_controlplan_parser(control_plan))
