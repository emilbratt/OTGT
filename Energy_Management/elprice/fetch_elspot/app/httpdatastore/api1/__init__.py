import requests

class Handle:

    EXPECTED_STATUS_CODES = [
        200, 201, 202
    ]

    def __init__(self, envar_get: object):
        self.URL_RAW = envar_get('WEB_DATASTORE_URL') + '/elspot/raw/v0'
        self.URL_RESHAPED = envar_get('WEB_DATASTORE_URL') + '/elspot/reshaped/v1'
        self.requests = requests
        self.log = False

    def send_raw(self, data_raw: dict) -> bool:
        try:
            payload =  {
                'data': data_raw,
                'date': data_raw['endDate'],
            }
            print('POST request', self.URL_RAW)
            r = self.requests.post(self.URL_RAW, json=payload)
            self.log = {
                'date': data_raw['endDate'],
                'request_method': 'POST',
                'request_url': self.URL_RAW,
                'response_code': r.status_code,
                'response_header': r.request.headers,
                'response_body': r.text,
            }
            return (r.status_code in self.EXPECTED_STATUS_CODES)
        except requests.exceptions.ConnectionError:
            self.log = {
                'namespace': 'httpdatastore.api1.send_raw()',
                'error': 'requests.exceptions.ConnectionError',
            }
        return False

    def raw_exists_on_datastore(self, isodate: str) -> bool:
        '''
            returns
                True if raw data already exist in web datastore
                False if it doesnt
        '''
        try:
            url = self.URL_RAW + '/' + isodate
            print('HEAD request', url)
            r = self.requests.head(url)
            self.log = {
                'request_method': 'HEAD',
                'request_url': url,
                'response_code': r.status_code,
                'response_header': r.request.headers,
            }
            return (r.status_code in self.EXPECTED_STATUS_CODES)
        except requests.exceptions.ConnectionError:
            self.log = {
                'namespace': 'httpdatastore.api1.raw_exists_on_datastore()',
                'error': 'requests.exceptions.ConnectionError',
            }
        return False

    def send_reshaped(self, data_reshaped: list) -> bool:
        try:
            payload =  {
                'data': data_reshaped,
                'date': data_reshaped[0]['date'],
            }
            print('POST request', self.URL_RESHAPED)
            r = self.requests.post(self.URL_RESHAPED, json=payload)
            self.log = {
                'date': data_reshaped[0]['date'],
                'request_method': 'POST',
                'request_url': self.URL_RESHAPED,
                'response_code': r.status_code,
                'response_header': r.request.headers,
                'response_body': r.text,
            }
            return (r.status_code in self.EXPECTED_STATUS_CODES)
        except requests.exceptions.ConnectionError:
            self.log = {
                'namespace': 'httpdatastore.api1.send_reshaped()',
                'error': 'requests.exceptions.ConnectionError',
            }
        return False

    def reshaped_exists_on_datastore(self, isodate: str) -> bool:
        '''
            returns
                True if raw data already exist in web datastore
                False if it doesnt
        '''
        try:
            url = self.URL_RESHAPED + '/' + isodate
            print('HEAD request', url)
            r = self.requests.head(url)
            self.log = {
                'request_method': 'HEAD',
                'request_url': url,
                'response_code': r.status_code,
                'response_header': r.request.headers,
            }
            return (r.status_code in self.EXPECTED_STATUS_CODES)
        except requests.exceptions.ConnectionError:
            self.log = {
                'namespace': 'httpdatastore.api1.reshaped_exists_on_datastore()',
                'error': 'requests.exceptions.ConnectionError',
            }
        return False
