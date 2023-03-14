import unittest


class Environment(unittest.TestCase):

    # testing if we have forgotten to configure cocuvida
    def test_cocuvida(self):
        from tests.environment_test import cocuvida
        cocuvida(self)

    # testing if we have forgotten to configure cocuvida
    def test_mqtt(self):
        from tests.environment_test import mqtt
        mqtt(self)


class Requirements(unittest.TestCase):

    # check if needed python modules are installed
    def test_requirements(self):
        from tests.requirements_test import check_modules
        check_modules(self)


class SQLDatabase(unittest.TestCase):

    # check if we can write the database file data.sqlite etc.
    def test_create_database(self):
        from tests.sqldatabase_test import create_database
        create_database(self)


class ControlPlan(unittest.TestCase):

    # check if we can write the database file data.sqlite etc.
    def test_example_controlplan(self):
        from tests.controlplan_test import example_controlplan
        example_controlplan(self)
    

if __name__ == '__main__':
    unittest.main()
