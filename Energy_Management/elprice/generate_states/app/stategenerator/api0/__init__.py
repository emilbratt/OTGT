from .process import percent, diff_factor, weight

class Handle:
    # data passed to generate states will need to have this structure
    '''
        {
            'region':    'Molde',
            'currency':  'NOK',
            'date':      'YYYY-MM-DD',
            'unit':      'ore/kWh',
            'max':       '280',
            'min':       '143',
            'average':   '197',
            'resolution': 96,
            'prices': [
                {'index': 0,  'time_start': '00:00', 'time_end': '00:15', 'value': '210'},
                {'index': 1,  'time_start': '00:15', 'time_end': '00:30', 'value': '190'},
                {'index': 2,  'time_start': '00:30', 'time_end': '00:45', 'value': '200'},
                ..,
                ..,
                {'index': 94, 'time_start': '23:30', 'time_end': '00:45', 'value': '239'},
                {'index': 95, 'time_start': '23:45', 'time_end': '00:00', 'value': '247'}
            ]
        }
    '''

    # after processing, an extra hashmap "states" will be created for each element in data['prices']
    '''
        prices[
            {
                'index': 0,
                'time_start': '00:00',
                'time_end': '00:15',
                'value': '210',
                'states': {
                    'key': 'val',
                    'key': 'val',
                    'key': 'val',
                    ..,
                }
            },
            {
                'index': 1,
                ..,
            },
            {
                'index': 2,
                ..,
            },

        ]

    '''
    def __init__(self, data: dict):
        # declaring variables to be used
        self.log = {}
        self.max = None # maximum price
        self.min = None # minimum price
        self.avg = None # average price
        self.date = None # date in ISO 8601 format e.g. YYYY-MM-DD
        self.resolution = None # price index resolution which ranges from 0 to N-1 e.g. if N = 96, then 0-95
        self.hours_from = []# list of hours from in format 'HH'
        self.hours_to   = []# list of hours to   in format 'HH'
        self.quarters_from = [] # list of quarters from in format 'HH:MM'
        self.quarters_to   = [] # list of quarters to   in format 'HH:MM'

        self.invalid_data = False # only process data if this is False

        # do some checks and initializations of variables
        try:
            # if all the values are cast-able to int, we are golden
            prices_value = [int(x['value']) for x in data['prices']]
            self.log['prices'] = True
        except:
            # likely dataset without prices, for some regions this occur
            self.log['prices'] = False
            self.invalid_data = True

        try:
            self.max = int(data['max'])
            self.min = int(data['min'])
            self.avg = int(data['average'])
            self.resolution = int(data['resolution'])
            self.log['convenient values'] = True
        except:
            self.log['convenient values'] = False
            self.invalid_data = True

        try:
            self.date = data['date']
            self.log['date'] = True
        except:
            self.log['date'] = False
            self.invalid_data = True

        try:
            self.hours_from = [x['time_start'][0:2] for x in data['prices'] if x['time_start'][3:] == '00']
            self.hours_to   = [x['time_end'][0:2]   for x in data['prices'] if x['time_end'][3:]   == '00']
            self.log['hours to and from'] = True
        except:
            self.log['hours to and from'] = False
            self.invalid_data = True

        try:
            self.quarters_from = [ x['time_start'] for x in data['prices'] ]
            self.quarters_to   = [ x['time_end']   for x in data['prices'] ]
            self.log['quarters to and from'] = True
        except:
            self.log['quarters to and from'] = False
            self.invalid_data = True

        # test if resolution matches indexes in prices list
        try:
            for index in range(data['resolution']):
                if data['prices'][index]['index'] != index:
                    self.invalid_data = True
                    self.log['mismatching resolution index'] = data['prices'][index]['index']
        except:
            self.log['resolution'] = False
            self.invalid_data = True


        self.data = data


    def generate(self) -> bool:
        if self.invalid_data:
            return False

        # add a hashmap for states for each index/price
        for index in range(self.resolution):
            self.data['prices'][index]['states'] = {}

        payload = {}

        self.data = percent(self.data)
        self.data = diff_factor(self.data)
        self.data = weight(self.data)
        if self.data['region'] == 'Molde':
            print(self.data)

        self.payload = self.data

        prices_index = [x['index'] for x in self.data['prices']]
        prices_value = [int(x['value']) for x in self.data['prices']]

        for index in prices_index:
            price = int(self.data['prices'][index]['value'])
            if price == int(self.data['max']):
                pass
            elif price == int(self.data['min']):
                pass
            elif price == int(self.data['average']):
                pass
            elif price > int(self.data['average']):
                pass
            elif price < int(self.data['average']):
                pass
        return True



        self.payload = { 
            'region': data['region'],
            'date': data['date'],
            'data': '<json_here>',
        }
        return True
