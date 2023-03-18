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


class ControlPlan(unittest.IsolatedAsyncioTestCase):

    # check if we can generate states from test control_plan
    async def test_generate_states(self):
        from tests.controlplan_test import generate_controlplan_states
        await generate_controlplan_states(self)



if __name__ == '__main__':
    unittest.main()
