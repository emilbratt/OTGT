from cocuvida.environment import env_ini_get


# if new configurations are implemented in app
# ..make sure they are also listed here
def cocuvida(self):
    # COCUVIDA configuration
    self.assertFalse(env_ini_get(section='cocuvida', key='host') == "INSERT")
    self.assertFalse(env_ini_get(section='cocuvida', key='port') == "INSERT")
    self.assertFalse(env_ini_get(section='cocuvida', key='secret') == "INSERT")

def mqtt(self):
    # MQTT configuration
    self.assertFalse(env_ini_get(section='mqtt', key='host') == "INSERT")
    self.assertFalse(env_ini_get(section='mqtt', key='port') == "INSERT")
    self.assertFalse(env_ini_get(section='mqtt', key='user') == "INSERT")
    self.assertFalse(env_ini_get(section='mqtt', key='password') == "INSERT")
