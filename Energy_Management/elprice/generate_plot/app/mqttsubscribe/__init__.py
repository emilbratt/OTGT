import paho.mqtt.client as mqtt

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

def mqttinit(envar_get: object,
             client_id: str,
             on_connect: object,
             on_message: object) -> object:
    port = 1883
    seconds_keepalive = 60
    client = mqtt.Client(client_id=envar_get('MQTT_CLIENT_ID_GENERATE_PLOT'), clean_session=False)
    client.username_pw_set(envar_get('MQTT_USER'), envar_get('MQTT_PW'))
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(envar_get('HOST_MQTT'), port, int(envar_get('MQTT_KEEP_ALIVE_SEC')))
    return client
