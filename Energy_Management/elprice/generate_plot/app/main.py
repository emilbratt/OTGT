from timehandle    import sleep, timeofday, isodate
from mqttsubscribe import mqttsubscribeinit
from plotgenerator import plotinit
from httpdatastore import httpdatastoreinit
from envars        import envar_get
import json

class Application:
    def __init__(self):
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
        print('MQTT Connected')
        print('RC:', str(rc))
        print('Client ID:', client._client_id.decode('utf8'))
        print('Flags:', flags)
        topic=envar_get('MQTT_TOPIC_ELPRICE_ELSPOT_RESHAPED')
        client.subscribe(topic=topic, qos=1)
        print('Subscribed (topic):', topic)

    # callback function for when we receive a message from broker
    def on_message(self, client, userdata, msg):
        print('Time:', isodate.today_seconds())
        print('MQTT Message')
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

        plot = plotinit(envar_get=envar_get)
        for region_data in data:
            print('generating day plot for', region_data['region'])
            if plot.generate_bar_chart_bydate(region_data):
                res = self.http.send_bydate(plot.payload)
                if not res:
                    print(self.http.log)
            else:
                print(region_data['region'], 'invalid data')

            print('generating hourly plots for', region_data['region'])
            if plot.generate_bar_chart_byhour(region_data):
                for payload in plot.payload:
                    res = self.http.send_byhour(payload)
                    if not res:
                        print(self.http.log)
            else:
                print(region_data['region'], 'invalid data')
        print('done')

def mainloop():
    print('Application starttime:', isodate.today_minutes())
    Application().loop_n_times(5)

mainloop()
