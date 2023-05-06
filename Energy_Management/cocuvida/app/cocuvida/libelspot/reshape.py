import json


async def reshape_dayahead(response_text: str) -> dict:
    '''
    pass the serialised json as the elspot_raw parameter
    if reshape success -> returns a list with dicts that looks like this

    below shows region struct layout with a bit more details for Molde region
    {
        'Bergen': {},
        'Molde': {
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
        'Oslo': {},
        '...': {},
        '...': {},
        '...': {},
    }

    if reshape fails -> returns empty dict {}

    NOTE: about daylight saving time
        if normal day (24 hours):
            extra row happens on index 24
        if swithcing to winter time (25 hours)
            extra row happens on index 25
        if switching to summer time (23 hours)
            row index 2 has no values
    '''
    try:
        elspot_raw = json.loads(response_text)
    except:
        print('ERROR: failed to load JSON from response_text')
        return {}

    regions = {}
    try:
        currency = elspot_raw['currency']
        match currency:
            case 'NOK':
                unit = 'øre/kWh'
            case 'EUR':
                unit = 'E.cent/kWh'
            case _:
                unit = elspot_raw['data']['Units'][0]

        for row in elspot_raw['data']['Rows'][0]['Columns']:
            region_name = row['Name']
            region_struct = {
                'region': region_name,
                'date': elspot_raw['data']['DataStartdate'].split('T')[0],
                'currency': currency,
                'unit': unit,
                'max': False,
                'min': False,
                'average': False,
                'resolution': 0,
                'prices': []
            }
            regions[region_name] = region_struct
    except:
        print('ERROR: failed to create region_struct')
        return {}
    # unpack data and assign to its correct region
    try:
        for row in elspot_raw['data']['Rows']:
            start_hour = row['StartTime'].split('T')[1][:2]
            end_hour   = row['EndTime'].split('T')[1][:2]
            for col in row['Columns']:
                region = col['Name']
                value = col['Value']
                value = value.replace(' ', '')
                value = value.replace(',', '.')
                try:
                    value = float(value)
                    match unit:
                        case 'øre/kWh'|'E.cent/kWh':
                            value = round(value*0.1)
                        case _:
                            value = round(value)
                except ValueError:
                    if start_hour == '02':
                        # if this happens -> likely means moving from winter-time to summer-time at 2 AM
                        # ..and that means there wont be any values between 02:00 and 03:00 as this hour is skipped
                        continue
                if row['IsExtraRow']:
                    title_name = row['Name']
                    regions[region][title_name.lower()] = value
                elif not row['IsExtraRow']:
                    # here is also where the increase in resolution happens (hour 4x -> quarters)
                    for j in range(4):
                        # work out time of day by adding 15, 30 or 45 minutes if needed
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

        ret_regions = {}
        # check if any regions have invalid price values
        for name in regions:
            price = regions[name]['prices'][0]['value']
            # nordpool sets price value to "-"" if no price, we dont want regions with no price
            if price != '-':
                # also, if price is not INT, dont want that either
                if isinstance(price, int):
                    # OK, we are got to go
                    ret_regions[name] = regions[name]

        return ret_regions
    except:
        print('ERROR: failed to process elspot data')
        return {}
