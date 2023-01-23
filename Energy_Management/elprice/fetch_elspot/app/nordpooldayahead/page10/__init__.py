from requests import get as http_GET

URL = 'https://www.nordpoolgroup.com/api/marketdata/page/10'

# just for testing (trying to be kind to the official api)
# REMEMBER TO REMOVE
URL = 'http://192.168.0.207:8082/download/hourly/2023-01-23.json'


class Handle:

    def __init__(self, envar_get: object):
        self.data_raw = False
        self.data_reshaped = False
        self.currency = envar_get('NORDPOOL_CURRENCY')
        self.unit = envar_get('NORDPOOL_UNIT')
        self.reshape_unit = envar_get('NORDPOOL_RESHAPE_UNIT')

    def fetch(self) -> int:
        params = { 'currency': self.currency }
        res = http_GET(URL, params=params, timeout=None)
        self.status_code = res.status_code
        if self.status_code == 200:
            self.data_raw = res.json()
            return True
        return False

    def confirm_date(self, isodate: str) -> bool:
        # expects tomorrows isodate in format 'YYYY-MM-DD'
        if isodate == self.data_raw['data']['DataStartdate'].split('T')[0]:
            return True
        return False

    def confirm_currency(self) -> bool:
        # expects currency as "NOK" e.g.
        if self.currency == self.data_raw['currency']:
            return True
        return False

    def confirm_unit(self) -> bool:
        # expects unit as "NOK/MWh" e.g.
        if self.unit == self.data_raw['data']['Units'][0]:
            return True
        return False

    def reshape_data(self) -> bool:
        '''
            takes the raw data and reshapes it into a json like associated array
            described like shown below
            {
                'region': {
                    'Molde': {
                        'currency': 'NOK',
                        'date':    'YYYY-MM-DD',
                        'unit':    'ore/kWh',
                        'Max':     '280',
                        'Min':     '143',
                        'Average': '197',
                        'quarters': [
                            {'index': 0, 'time_start': '00:00', 'time_end': '00:15', 'value': '210'},
                            {'index': 1, 'time_start': '00:15', 'time_end': '00:30', 'value': '210'},
                            ..,
                            {'index': 95, 'time_start': '23:45', 'time_end': '00:00', 'value': '247'}
                        ]
                    },
                    '<region>': {
                        ..
                    },
                    '<region>': {
                        ..
                    },
                }
            }
        '''
        regions = {}
        for row in self.data_raw['data']['Rows'][0]['Columns']:
            arr_scaffold = {
                'currency': self.data_raw['currency'],
                'date': self.data_raw['data']['DataStartdate'].split('T')[0],
                'unit': self.reshape_unit,
                'max': False,
                'min': False,
                'average': False,
                'quarters': []
            } # keep key-names like so, otherwise they will not match dataset
            region = row['Name']
            regions[region] = arr_scaffold

        for row_number,row in enumerate(self.data_raw['data']['Rows']):
            start_hour = row['StartTime'].split('T')[1][:2]
            end_hour   = row['EndTime'].split('T')[1][:2]
            title_name = row['Name'] # avg, min or html special char for hour
            for col in self.data_raw['data']['Rows'][row_number]['Columns']:
                region = col['Name']
                value = col['Value']
                if self.reshape_unit == 'ore/kWh':
                    value = value.replace(' ', '')
                    value = value.replace(',', '.')
                    try:
                        value = float(value)
                        value = round(value*0.1)
                    except ValueError:
                        pass
                if row['IsExtraRow']:
                    regions[region][title_name.lower()] = value
                else:
                    # here is also where the increase in resolution happens (hour 4x -> quarters)
                    for j in range(4):
                        # work out timestamp for each 15 minutes
                        start = str(start_hour) + ':' + str(j * 15).zfill(2)
                        if j == 3:
                            end = str(end_hour) + ':00'
                        else:
                            end = str(start_hour) + ':' + str((j+1) * 15).zfill(2)

                        quarter_row_number = int((row_number*4) + j)
                        price = {
                            'index': quarter_row_number,
                            'time_start': str(start),
                            'time_end': str(end),
                            'value': value
                        }
                        regions[region]['quarters'].append(price)

        self.data_reshaped = regions
        return True
