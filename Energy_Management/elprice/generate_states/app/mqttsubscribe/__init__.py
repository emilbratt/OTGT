import paho.mqtt.client as mqtt
import configparser

# about "clean_session" and durable/non-durable clients
#   True:
#     for none durable clients
#     used if client only publish messages or for testing/dev
#     broker does not store undelivered messages
#     broker does not store client information (client id etc.)
#   False:
#     for durable cients
#     if client must receive (almost) all messages or if bad connection
#     broker keeps undelivered messages (delivered messages are still removed)
#     however, client must use QoS level 1 or 2 for pub and sub messages
#     also, also, for others to recieve this clients published messagesn
#     ..use retain=True like below
#       client.publish(topic=topic, payload=payload, qos=1, retain=True)


def mqttsubscribeinit(envar_get: object, on_connect: object, on_message: object) -> object:
    MQTT_CLIENT_ID = envar_get('MQTT_CLIENT_ID')
    config = configparser.ConfigParser()
    config.sections()
    config.read(envar_get('ENVIRONMENT_INI_FILE'))
    section = config['mqtt']
    MQTT_HOST = section['host'].strip('"')
    MQTT_PORT = int(section['port'].strip('"'))
    MQTT_USER = section['user'].strip('"')
    MQTT_PW   = section['password'].strip('"')

    client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=False)
    client.username_pw_set(MQTT_USER, MQTT_PW)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT)
    return client
