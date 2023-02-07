from paho.mqtt import publish

def mqttmessage(envar_get: object, topic: str, datamodel: object, qos: int) -> bool:
    host = envar_get('HOST_MQTT')
    client_id = envar_get('MQTT_CLIENT_ID_WEB_DATASTORE')
    authentication = {
        'username': envar_get('MQTT_USER'),
        'password': envar_get('MQTT_PW'),
    }
    use_tls = None
    transport = 'tcp'
    port = 1883
    retain = False
    will = None
    keep_alive = 60

    payload = False
    try:
        payload = datamodel.get_json_data()
    except:
        payload = datamodel.data
    if payload == False:
        print('NO MESSAGE IN DATAMODEL TO PUBLISH')
        return False
    publish.single(
                    topic=topic,
                    payload=payload,
                    qos=qos,
                    retain=retain,
                    hostname=host,
                    port=port,
                    client_id=client_id,
                    keepalive=keep_alive,
                    will=will,
                    auth=authentication,
                    tls=use_tls,
                    transport=transport
                    )
