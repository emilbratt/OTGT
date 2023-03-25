from requests import get

class Handle:

    def __init__(self, envar_get: object, isodate: object, url: str):
        self.isodate = isodate
        self.url = url
        self.log = False
        self.data_raw = False
        self.data_reshaped = False
        self.date_tomorrow = False
        self.namespace = 'nordpooldayahead.api1'
        self.currency = envar_get('NORDPOOL_CURRENCY')
        self.unit = envar_get('NORDPOOL_UNIT')
        self.reshape_unit = envar_get('NORDPOOL_RESHAPE_UNIT')

    def fetch_data(self) -> bool:
        '''
            isodate in format YYYY-MM-DD e.g. '2023-01-30'
        '''
        self.date_tomorrow = self.isodate.today_plus_days(1)
        params = {
            'currency': self.currency,
            'endDate': self.date_tomorrow,
        }
        r = get(self.url, params=params, timeout=None)
        self.status_code = r.status_code
        if self.status_code == 200:
            self.data_raw = r.json()
            return True
        self.log = {
            'request_method': 'POST',
            'request_url': self.url,
            'response_code': r.status_code,
            'response_header': r.request.headers,
        }
        return False

    def confirm_date(self) -> bool:
        # expects tomorrows isodate in format 'YYYY-MM-DD'
        self.log = {
            'namespace': self.namespace + '.confirme_date()',
        }
        try:
            if self.date_tomorrow == self.data_raw['data']['DataStartdate'].split('T')[0]:
                return True
            else:
                self.log['isodate'] = self.date_tomorrow
                self.log['date on received data'] = self.data_raw['data']['DataStartdate'].split('T')[0]
        except:
            self.log['isodate'] = self.date_tomorrow
            self.log['date on received data'] = 'could not extract'
        return False

    def confirm_currency(self) -> bool:
        # expects currency as "NOK" e.g.
        if self.currency == self.data_raw['currency']:
            return True
        self.log = {
            'currency': self.currency,
            'currency on received data': self.data_raw['currency'],
        }
        return False

    def confirm_unit(self) -> bool:
        # expects unit as "NOK/MWh" e.g.
        if self.unit == self.data_raw['data']['Units'][0]:
            return True
        self.log = {
            'unit': self.unit,
            'unit on received data': self.data_raw['data']['Units'][0],
        }
        return False

    def reshape_data(self) -> bool:
        # takes the raw data and reshapes it into a json like list
        # with associated arrays described graphically below
        '''
        [
            {
                'region': 'Molde,
                'currency': 'NOK',
                'date':    'YYYY-MM-DD',
                'unit':    'ore/kWh',
                'Max':     '280',
                'Min':     '143',
                'Average': '197',
                'resolution': 96,
                'prices': [
                    {'index': 0, 'time_start': '00:00', 'time_end': '00:15', 'value': '210'},
                    {'index': 1, 'time_start': '00:15', 'time_end': '00:30', 'value': '210'},
                    ..,
                    {'index': 95, 'time_start': '23:45', 'time_end': '00:00', 'value': '247'}
                ]
            },
            {..},
            {..},
        ]

        NOTE: about daylight saving time
            if normal day (24 hours):
                extra row happens on index 24
            if swithcing to winter time (25 hours)
                extra row happens on index 25
            if switching to summer time (23 hours)
                row index 2 has no values
        '''
        # extract all regions, as this is needed as first step
        regions = {}
        try:
            for row in self.data_raw['data']['Rows'][0]['Columns']:
                arr_scaffold = {
                    'region': row['Name'],
                    'date': self.data_raw['data']['DataStartdate'].split('T')[0],
                    'currency': self.data_raw['currency'],
                    'unit': self.reshape_unit,
                    'max': False,
                    'min': False,
                    'average': False,
                    'resolution': 0,
                    'prices': []
                } # keep key-names like so, otherwise they will not match dataset
                region = row['Name']
                regions[region] = arr_scaffold
        except:
            self.log = {
                'received data': self.data_raw,
                'error': 'failed when creating regions array',
            }
            return False
        # unpack data and assign to its correct region
        try:
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
                            if start_hour == '02':
                                # if this happens -> likely means moving from winter-time to summer-time at 2 AM
                                # ..and that means there wont be any values between 02:00 and 03:00 as this hour is skipped
                                continue
                    if row['IsExtraRow']:
                        regions[region][title_name.lower()] = value
                    elif not row['IsExtraRow']:
                        # here is also where the increase in resolution happens (hour 4x -> quarters)
                        for j in range(4):
                            # work out timestamp for each 15 minutes
                            start = str(start_hour) + ':' + str(j * 15).zfill(2)
                            if j == 3:
                                end = str(end_hour) + ':00'
                            else:
                                end = str(start_hour) + ':' + str((j+1) * 15).zfill(2)

                            # the current resolution value (incr. +1 each time, can be appended as index)
                            index = regions[region]['resolution']
                            price = {
                                'index': index,
                                'time_start': str(start),
                                'time_end': str(end),
                                'value': value
                            }
                            regions[region]['resolution'] += 1
                            regions[region]['prices'].append(price)

            # convert the data structure to the final one where each region (dict) is a list object
            self.data_reshaped = []
            for region in regions:
                self.data_reshaped.append( regions[region] )
            return True
        except:
            self.log = {
                'received data': self.data_raw,
                'error': 'failed when reshaping data into regions array',
            }
            return False
