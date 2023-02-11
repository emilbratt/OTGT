import requests

class Handle:

    EXPECTED_STATUS_CODES = [
        200, 201, 202
    ]

    def __init__(self, envar_get: object):
        self.URL_BYDATE = envar_get('WEB_DATASTORE_URL') + '/states/bydate/v0'
        self.requests = requests

    def send(self, payload: dict) -> bool:
        '''
            payload structure
            {
                'date': '2023-01-23',
                'region': 'Molde',
                'data': '<json-string>',
            }
        '''
        print('skip sending for now and return True')
        return True
        self.log = {}
        try:
            print('POST request', self.URL_BYDATE)
            print('Region', payload['region'], 'Date', payload['date'])
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
