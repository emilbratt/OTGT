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


class SQLDatabase(unittest.TestCase):

    # check if we can write the database file data.sqlite etc.
    def test_create_database(self):
        from tests.sqldatabase_test import create_database
        create_database(self)


class ControlPlan(unittest.TestCase):

    # check if we can generate states from test control_plan
    def test_example_controlplan(self):
        from tests.controlplan_test import example_controlplan
        example_controlplan(self)


class ElspotTest(unittest.TestCase):

    # check if we can reshape elspot prices for 23, 24 and 25 hour days (dst)
    def test_process_reshape_elspot(self):
        from tests.elspot_test import process_reshape_elspot
        process_reshape_elspot(self)


if __name__ == '__main__':
    unittest.main()
