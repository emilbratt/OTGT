import requests

class Handle:

    EXPECTED_STATUS_CODES = [
        200, 201, 202
    ]

    def __init__(self, envar_get: object):
        self.URL_BYDATE = envar_get('WEB_DATASTORE_URL') + '/plot/bydate/v0'
        self.URL_BYHOUR = envar_get('WEB_DATASTORE_URL') + '/plot/byhour/v0'
        self.requests = requests

    def send_bydate(self, payload: dict) -> bool:
        '''
            payload structure
            {
                'date': '2023-01-23',
                'region': 'Molde',
                'data': <svg-string>,
            }
        '''
        self.log = {}
        try:
            r = self.requests.post(self.URL_BYDATE, json=payload)
            self.log['date'] = payload['date']
            self.log['region'] = payload['region']
            self.log['request_method'] = 'POST'
            self.log['request_url'] = self.URL_BYDATE
            self.log['response_code'] = r.status_code
            self.log['response_header'] = r.request.headers
            self.log['response_body'] = r.text
            return (r.status_code in self.EXPECTED_STATUS_CODES)
        except requests.exceptions.ConnectionError:
            self.log['error'] = 'requests.exceptions.ConnectionError'
            self.log['namespace'] = 'httpdatastore.api0.send_bydate()'
        return False

    def send_byhour(self, payload: dict) -> bool:
        '''
            payload structure
            {
                'region': 'Molde',
                'date': '2023-01-23',
                'index': 0,
                'hour':  0,
                'data':  <svg-string>,
            }
        '''
        self.log = {}
        try:
            r = self.requests.post(self.URL_BYHOUR, json=payload)
            self.log['date'] = payload['date']
            self.log['region'] = payload['region']
            self.log['index'] = payload['index']
            self.log['hour'] = payload['hour']
            self.log['request_method'] = 'POST'
            self.log['request_url'] = self.URL_BYHOUR
            self.log['response_code'] = r.status_code
            self.log['response_header'] = r.request.headers
            self.log['response_body'] = r.text
            return (r.status_code in self.EXPECTED_STATUS_CODES)
        except requests.exceptions.ConnectionError:
            self.log = {
                'namespace': 'httpdatastore.api0.send_reshaped()',
                'error': 'requests.exceptions.ConnectionError',
            }
        return False
