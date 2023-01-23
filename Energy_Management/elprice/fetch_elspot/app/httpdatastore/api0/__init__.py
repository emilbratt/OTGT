import requests

class Handle:
    def __init__(self, envar_get: object):
        self.send_complete = False
        self.URL = envar_get('WEB_DATASTORE_URL')

    def send_raw(self, data: object) -> bool:
        '''
            send raw json data to datastore
        '''
        return True

    def send_reshaped(self, data: object) -> bool:
        '''
            send reshaped json data to datastore
        '''
        return True
