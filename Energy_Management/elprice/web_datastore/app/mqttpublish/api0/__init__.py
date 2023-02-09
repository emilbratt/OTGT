from paho.mqtt import publish
import configparser

class Publish:

    def __init__(self, envar_get: object):
        environment_ini = envar_get('ENVIRONMENT_INI_FILE')
        config = configparser.ConfigParser()
        config.sections()
        config.read(environment_ini)
        section = config['mqtt']
        self.MQTT_HOST = section['host'].strip('"')
        self.MQTT_PORT = int(section['port'].strip('"'))
        self.MQTT_USER = section['user'].strip('"')
        self.MQTT_PW   = section['password'].strip('"')
        self.MQTT_CLIENT_ID = envar_get('MQTT_CLIENT_ID')


    def single(self, topic: str, payload: str, qos: int) -> bool:
        use_tls = None
        transport = 'tcp'
        retain = False
        will = None
        keep_alive = 60
        publish.single(
                        topic=topic,
                        payload=payload,
                        qos=qos,
                        retain=retain,
                        hostname=self.MQTT_HOST,
                        port=self.MQTT_PORT,
                        client_id=self.MQTT_CLIENT_ID,
                        keepalive=keep_alive,
                        will=will,
                        auth={ 'username': self.MQTT_USER, 'password': self.MQTT_PW, },
                        tls=use_tls,
                        transport=transport
                        )
