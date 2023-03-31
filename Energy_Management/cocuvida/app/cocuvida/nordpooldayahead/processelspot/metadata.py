from statistics import mean

# these methods expects the processed elspot data structure for a single region as shown below
'''
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
    }
'''


async def percent(data: dict) -> dict:
    '''
        min price = 0%
        max price = 100%
        other prices = between 0% and 100%

        if we have many prices < 50%
            this means we have price spikes in the higher range (pyramid curve)
            longer period of below average prices
            fewer "very high" prices

        if we have many prices > 50%
            price spikes in the lower range (valley curve)
            longer period of above average prices
            fewer "very low" prices

        if we have many prices split apart (e.g. < 30% and > 70%)
            higher fluctuation between high and low prices
            prices vary alot throughout the day
    '''
    # for index in range(data['resolution']):
    for entry in data['prices']:
        index = entry['index']
        price = entry['value']
        if price == data['max']:
            percent = 100
        elif price == data['min']:
            percent = 0
        else:
            try:
                percent = (price-data['min']) * (100 / (data['max']-data['min']))
            except ZeroDivisionError:
                # if max and min are same (flat price curve), all prices are 100%
                percent = 100
        data['prices'][index]['percent'] = int(percent)
    return data

async def diff_factor(data: dict) -> dict:
    '''
        higher diff factors means higher fluctuation
        ranges from: 1
        min price = 1
        if max price = 4 -> max price is 4 times higher than min price

        handling negative numbers:
            we create an offset from the minimum value so that it becomes
            positive thus creating a fix for the calculation
    '''

    # force all values to be positive by adding an offset value
    add_val = 0
    if data['min'] <= 0:
        add_val = 1 + abs(data['min'])

    min_val = data['min'] + add_val
    for entry in data['prices']:
        index = entry['index']
        price = entry['value'] + add_val
        diff_factor = round(price/min_val, 2)
        data['prices'][index]['diff_factor'] = diff_factor
    return data

async def weight(data: dict) -> dict:
    '''
        max price weight = 10 
        min price weight = 0

        high fluctuation -> weights spread out between 0 and 10
        low fluctuation  -> many weights close to 10
        flat price curve -> all weights will be 10

        quick summary
            weight = 2.5   ->  price =  25% of max price
            weight = 5     ->  price =  50% of max price
            weight = 7.5   ->  price =  75% of max price

    '''
    _max_ = data['max']
    _min_ = data['min']
    add_val = 0
    if _min_ < 1:
        while _min_ < 1:
            add_val += 1
    _max_ += add_val
    _min_ += add_val
    for entry in data['prices']:
        index = entry['index']
        price = entry['value'] + add_val
        weight = round((price/_max_) * 10)
        data['prices'][index]['weight'] = weight
    return data

async def slope(data: dict) -> int:
    '''
        used to move priority towards the lower end

        range from 1 (flat)
        if:
            slope = 1.5 -> max price is  50% more than mean e.g. 150 to 100
            slope = 2.0 -> max price is 100% more than mean e.g. 200 to 100
            slope = 2.5 -> max price is 250% more than mean e.g. 250 to 100
        ..spikes and dips only affect the slope by a small margin as it is based on the mean value
    '''

    price_list = [x['value'] for x in data['prices']]
    # push all numbers to a positive value if needed
    _min_ = min(price_list)
    if _min_ < 0:
        new_list = []
        offset = 0
        while _min_ < 1:
            offset += 1
            _min_ += 1
        for val in price_list:
            new_list.append(val+offset)
        price_list = new_list
    _mean_ = mean(price_list)
    _max_ = max(price_list)
    _min_ = min(price_list)
    try:
        slope = round((_max_ / _mean_), 1)
    except ZeroDivisionError:
        slope = 1.0
    return float(slope)

async def spike(data: dict) -> int:
    '''
        used to
            ..reduce priority on the higher values if positive
            ..increase priority on the lower values if negative

        range from - (dip) to + (spike)
             -N
            -50 = massive dip
            -10 = small dip
              0 = no spike
            +10 = small spike
            +50 = massive spike
             +N

        difference between mean, min and max value is calculated
    '''

    price_list = [x['value'] for x in data['prices']]
    # force push all numbers to a positive value
    _min_ = min(price_list)
    if _min_ < 0:
        new_list = []
        offset = 0
        while _min_ < 1:
            offset += 1
            _min_ += 1
        for val in price_list:
            new_list.append(val+offset)
        price_list = new_list
    _mean_ = round(mean(price_list))
    _max_ = max(price_list)
    _min_ = min(price_list)
    spike = (_max_ - _mean_) - (_mean_ - _min_)
    try:
        slope = _max_ / _mean_
    except ZeroDivisionError:
        slope = 1.0
    spike = round(spike/slope)
    return spike
