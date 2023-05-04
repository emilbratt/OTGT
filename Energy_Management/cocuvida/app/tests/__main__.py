import unittest


class Environment(unittest.TestCase):

    # check if we have configured cocuvida
    def test_environment_cocuvida(self):
        from tests import environment_test
        environment_test.cocuvida(self)

    # check if we have configured cocuvida
    def test_environment_mqtt(self):
        from tests import environment_test
        environment_test.mqtt(self)


class Requirements(unittest.TestCase):

    # check if all python dependencies are installed
    def test_import_requirements(self):
        from tests import requirements_test
        requirements_test.check_modules(self)


class ControlPlan(unittest.TestCase):

    # check if we can generate states from test control_plan
    def test_example_controlplan(self):
        from tests import controlplan_test
        controlplan_test.test_controlplan(self, file_ref='example_controlplan', operation_date='2022-12-01')
        controlplan_test.test_controlplan(self, file_ref='example_elspot', operation_date='2022-12-01')
        controlplan_test.test_controlplan(self, file_ref='example_elspot', operation_date='2023-03-26')
        controlplan_test.test_controlplan(self, file_ref='example_elspot', operation_date='2022-10-30')
        controlplan_test.test_controlplan(self, file_ref='example_elspot', operation_date='2023-04-10')

class ElspotTest(unittest.TestCase):

    # check if we can process elspot prices for 23, 24 and 25 hour days (dst)
    def test_processelspot(self):
        from tests import elspot_test
        elspot_test.process_elspot(self, file_ref='23', expected_resolution=92)
        elspot_test.process_elspot(self, file_ref='25', expected_resolution=100)
        elspot_test.process_elspot(self, file_ref='normal', expected_resolution=96)
        elspot_test.process_elspot(self, file_ref='negative', expected_resolution=96)


if __name__ == '__main__':
    from cocuvida.sqldatabase import scripts
    # first: create database and tables if not exist
    res = scripts.run('create_tables.sql')
    if not res:
        exit(1)
    # second: run all tests
    unittest.main()
