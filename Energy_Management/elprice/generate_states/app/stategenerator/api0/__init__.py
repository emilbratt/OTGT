import numpy as np

class State:
    def __init__(self, envar_get: object):
        # data passed to generate states will need to have this structure
        '''
        {
            'region':    'Molde,
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
        self.envar_get = envar_get
        self.log = False


    def generate(self, data: dict) -> bool:
        self.payload = {}
        prices_index = [x['index'] for x in data['prices']]
        try:
            prices_value = [int(x['value']) for x in data['prices']]
        except:
            # likely dataset without prices, for some regions this occur
            return False

        for index in prices_index:
            price = int(data['prices'][index]['value'])
            if price == int(data['max']):
                pass
            elif price == int(data['min']):
                pass
            elif price == int(data['average']):
                pass
            elif price > int(data['average']):
                pass
            elif price < int(data['average']):
                pass

        hours_from = [int(x['time_start'][0:2]) for x in data['prices'] if x['time_start'][3:] == '00']
        hours_to   = [int(x['time_end'][0:2])   for x in data['prices'] if x['time_end'][3:]   == '00']

        quarters_from = [ x['time_start'] for x in data['prices'] ]
        quarters_to   = [ x['time_end']   for x in data['prices'] ]

        self.payload = { 
            'region': data['region'],
            'date': data['date'],
            'data': '<json_here>',
        }
        return True
