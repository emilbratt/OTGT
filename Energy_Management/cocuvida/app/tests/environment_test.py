import unittest

from cocuvida.environment import env_ini_get, env_var_get

VALID_CURRENCY_LIST = ('NOK', 'EUR')


# if new configurations are implemented in app
# ..make sure they are also listed here
def cocuvida(self: unittest.TestCase):
    # COCUVIDA configuration
    self.assertFalse(env_ini_get(section='cocuvida', key='host') == "INSERT")
    self.assertFalse(env_ini_get(section='cocuvida', key='port') == "INSERT")
    self.assertFalse(env_ini_get(section='cocuvida', key='secret') == "INSERT")

    # validate elspot_currency
    currency = env_ini_get(section='cocuvida', key='elspot_currency')
    self.assertTrue(currency in VALID_CURRENCY_LIST)

    # envar COCUVIDA_TESTING should be true (in production it is false or not set)
    self.assertTrue(env_var_get('COCUVIDA_TESTING'))

def mqtt(self: unittest.TestCase):
    # MQTT configuration
    self.assertFalse(env_ini_get(section='mqtt', key='host') == "INSERT")
    self.assertFalse(env_ini_get(section='mqtt', key='port') == "INSERT")
    self.assertFalse(env_ini_get(section='mqtt', key='user') == "INSERT")
    self.assertFalse(env_ini_get(section='mqtt', key='password') == "INSERT")
