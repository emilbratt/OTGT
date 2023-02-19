from timehandle     import sleep, timeofday, isodate
from mqttsubscribe  import mqttsubscribeinit
from httpdatastore  import httpdatastoreinit
from stategenerator import stateinit
from envars         import envar_get
import json

class Application:
    def __init__(self):
        self.states = stateinit(envar_get=envar_get)
        self.http = httpdatastoreinit(envar_get=envar_get)
        self.client = mqttsubscribeinit(envar_get=envar_get,
                                        on_connect=self.on_connect,
                                        on_message=self.on_message)

    def loop_forever(self):
        self.client.loop_forever()

    def loop_n_times(self, n: int):
        while n > 0:
            self.client.loop_start()
            self.client.loop_stop()
            print('round ' + str(n))
            n -= 1
            sleep.seconds(2)

    def dummy_daemon(self):
        while True:
            print('just sleeping')
            sleep.seconds(3600)

    # callback function for when we receive a CONNACK from broker
    def on_connect(self, client, userdata, flags, rc):
        print('Time:', isodate.today_seconds())
        print('MQTT Connection established')
        print('RC:', str(rc))
        print('Client ID:', client._client_id.decode('utf8'))
        print('Flags:', flags)
        topic=envar_get('MQTT_TOPIC_ELPRICE_ELSPOT_RESHAPED')
        client.subscribe(topic=topic, qos=1)
        print('Subscribed (topic):', topic)

    # callback function for when we receive a message from broker
    def on_message(self, client, userdata, msg):
        print('Time:', isodate.today_seconds())
        print('MQTT Message Received')
        try:
            data = msg.payload.decode('utf-8')
            data = json.loads(data)
        except:
            try:
                print('paload is not valid json')
                print('pyload', msg.payload.decode('utf-8'))
            except:
                print('error:')
                print('the data received could not be processed')
            return False

        for region_data in data:
            print('generating power states for', region_data['region'])
            states = self.states(region_data)
            is_generated = states.generate()
            if is_generated:
                pass
                is_sent = self.http.send(states.payload)
                if is_sent:
                    print('OK')
                else:
                    print(self.http.log)
            else:
                print(states.log)

def mainloop():
    print('Application starttime:', isodate.today_minutes())
    Application().loop_forever()

mainloop()
