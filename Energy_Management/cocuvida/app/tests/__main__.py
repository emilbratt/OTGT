import unittest


class Environment(unittest.TestCase):

    # testing if we have forgotten to configure cocuvida
    def test_environment_cocuvida(self):
        from tests.environment_test import cocuvida
        cocuvida(self)

    # testing if we have forgotten to configure cocuvida
    def test_environment_mqtt(self):
        from tests.environment_test import mqtt
        mqtt(self)


class Requirements(unittest.TestCase):

    # check if needed python modules are installed
    def test_import_requirements(self):
        from tests.requirements_test import check_modules
        check_modules(self)


class ControlPlan(unittest.TestCase):

    # check if we can generate states from test control_plan
    def test_example_controlplan(self):
        from tests.controlplan_test import example_controlplan
        example_controlplan(self)


class ElspotTest(unittest.TestCase):

    # check if we can reshape elspot prices for 23, 24 and 25 hour days (dst)
    def test_processelspot(self):
        from tests.elspot_test import process_elspot
        process_elspot(self, hour=23, expected_resolution=92)
        process_elspot(self, hour=24, expected_resolution=96)
        process_elspot(self, hour=25, expected_resolution=100)


if __name__ == '__main__':
    from cocuvida.sqldatabase import scripts
    # first: create database and tables if not exist
    res = scripts.run('create_tables.sql')
    if not res:
        exit(1)
    # second: run all tests
    unittest.main()
