import requests

class Handle:

    EXPECTED_STATUS_CODES = [
        200, 201, 202
    ]

    def __init__(self, envar_get: object):
        self.send_complete = False
        self.URL_RESHAPED = envar_get('WEB_DATASTORE_URL') + '/elspot/reshaped'
        self.URL_RAW = envar_get('WEB_DATASTORE_URL') + '/elspot/raw'
        self.requests = requests
        self.log = False

    def raw_exists_on_datastore(self, isodate: str) -> bool:
        '''
            returns
                True if raw data already exist in web datastore
                False if it doesnt
        '''
        url = self.URL_RAW + '/' + isodate
        r = self.requests.head(url)
        self.log = {
            'request_method': 'HEAD',
            'request_url': url,
            'response_code': r.status_code,
            'response_header': r.request.headers,
        }
        return (r.status_code in self.EXPECTED_STATUS_CODES)


    def send_raw(self, data: object) -> bool:
        try:
            payload =  {
                'data': data,
                'date': data['endDate'],
            }
            r = self.requests.post(self.URL_RAW, json=payload)
            self.log = {
                'date': data['endDate'],
                'request_method': 'POST',
                'request_url': self.URL_RAW,
                'response_code': r.status_code,
                'response_header': r.request.headers,
                'response_body': r.text,
            }
            return (r.status_code in self.EXPECTED_STATUS_CODES)
        except requests.exceptions.ConnectionError:
            return False

    def reshaped_exists_on_datastore(self, isodate: str) -> bool:
        '''
            returns
                True if raw data already exist in web datastore
                False if it doesnt
        '''
        url = self.URL_RESHAPED + '/' + isodate
        r = self.requests.head(url)
        self.log = {
            'request_method': 'HEAD',
            'request_url': url,
            'response_code': r.status_code,
            'response_header': r.request.headers,
        }
        return (r.status_code in self.EXPECTED_STATUS_CODES)

    def send_reshaped(self, data: object) -> bool:
        try:
            for region in data:
                payload =  {
                    'data': data[region],
                    'region': region,
                    'date': data[region]['date'],
                }
                r = self.requests.post(self.URL_RESHAPED, json=payload)
                self.log = {
                    'region': region,
                    'date': data[region]['date'],
                    'request_method': 'POST',
                    'request_url': self.URL_RAW,
                    'response_code': r.status_code,
                    'response_header': r.request.headers,
                    'response_body': r.text,
                }
                if r.status_code not in self.EXPECTED_STATUS_CODES:
                    return False
            return True
        except requests.exceptions.ConnectionError:
            return False
