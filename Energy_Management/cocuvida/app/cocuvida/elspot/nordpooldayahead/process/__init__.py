import json

from cocuvida.environment import env_ini_get

from . import NOK


async def reshape(elspot_raw: str):
    '''
    pass the serialised json as the elspot_raw parameter
    if reshape success -> returns a list with dicts that looks like this
    [
        {..},
        {
            'region': 'Molde,
            'currency': 'NOK',
            'date':    'YYYY-MM-DD',
            'unit':    'ore/kWh',
            'max':     '280',
            'min':     '143',
            'average': '197',
            'resolution': 96, # (92 for 23 hours, 100 for 25 hours)
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
    if reshape fails -> returns empty list []

    NOTE: about daylight saving time
        if normal day (24 hours):
            extra row happens on index 24
        if swithcing to winter time (25 hours)
            extra row happens on index 25
        if switching to summer time (23 hours)
            row index 2 has no values
    '''
    elspot_raw = json.loads(elspot_raw)
    currency = elspot_raw['currency']

    match currency:
        case 'NOK':
            data = await NOK.reshape(elspot_raw)
        case _:
            raise Exception('InvalidCurrency', currency)
    return data