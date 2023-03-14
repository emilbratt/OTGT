from cocuvida.environment import env_ini_get
from cocuvida.elspot.currency import (get as get_region_config, msg_valid_keys)


# if new configurations are implemented in app
# ..make sure they are also listed here
def cocuvida(self):
    # COCUVIDA configuration
    self.assertFalse(env_ini_get(section='cocuvida', key='host') == "INSERT")
    self.assertFalse(env_ini_get(section='cocuvida', key='port') == "INSERT")
    self.assertFalse(env_ini_get(section='cocuvida', key='secret') == "INSERT")
    self.assertFalse(env_ini_get(section='cocuvida', key='elspot_currency') == "INSERT")

    # validate elspot_currency
    validate_elspot_currency = get_region_config()
    self.assertTrue((validate_elspot_currency != False), msg=msg_valid_keys())

def mqtt(self):
    # MQTT configuration
    self.assertFalse(env_ini_get(section='mqtt', key='host') == "INSERT")
    self.assertFalse(env_ini_get(section='mqtt', key='port') == "INSERT")
    self.assertFalse(env_ini_get(section='mqtt', key='user') == "INSERT")
    self.assertFalse(env_ini_get(section='mqtt', key='password') == "INSERT")
