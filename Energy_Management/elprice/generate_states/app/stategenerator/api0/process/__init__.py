def percent(data: dict) -> dict:
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
    for index in range(data['resolution']):
        price = data['prices'][index]['value']
        if price == data['max']:
            percent = 100
        elif price == data['min']:
            percent = 0
        else:
            try:
                percent = (price-data['min']) * (100 / (data['max']-data['min']))
            except ZeroDivisionError:
                percent = 100
        data['prices'][index]['states']['percent'] = int(percent)
    return data


def diff_factor(data: dict) -> dict:
    '''
        higher diff factors means higher fluctuation

        lower diff_factor = better
        ranges from: 1
        min price = 1

        if price = 750 and min = 250 -> diff_factor = 3
            higher diff_factor means a higher difference between this and the lowest price

        if the highest price has a diff_factor = 4
            that means the highest price is 4 times higher than the lowest price

        for negative numbers, we create an offset from the minimum value
        so that it becomes positive thus creating a fix for the calculation
    '''

    # handle case if any negative number or if minimum price = 0
    add_val = 0
    if data['min'] <= 0:
        add_val = 1 + abs(data['min'])

    min_val = data['min'] + add_val
    for index in range(data['resolution']):
        price = data['prices'][index]['value'] + add_val
        diff_factor = round(price/min_val, 2)
        data['prices'][index]['states']['diff_factor'] = diff_factor
    return data


def weight(data: dict) -> dict:
    '''
        max price = 0
        min price = 1 (if positive) else > 1

        ranges from: 0 to approaching 1 (or exceeding 1 for prices < 1 including negative)

        the further the price weight is from 0 the better it is and
        the more inclined you would be to turn ON a power-hungry device

        or for the opposite situation, closer to 0 means more power saved leaving device OFF

        a high fluctuation scenario
            -> yields weights around 0 to 0.6+
        a little to no fluctuation scenario
            -> yields weights around 0 to 0.3-ish or less

        quick summary..
            weight = 0     ->  price = 100% of max price
            weight = 0.25  ->  price =  75% of max price
            weight = 0.33  ->  price =  66% of max price
            weight = 0.5   ->  price =  50% of max price
            weight = 0.66  ->  price =  33% of max price
            weight = 0.75  ->  price =  25% of max price
            weight = 1     ->  price =   0% of max price
            weight > 1     ->  price < 1 (can also be negative value)
    '''
    for index in range(data['resolution']):
        price = data['prices'][index]['value']
        try:
            data['prices'][index]['states']['weight'] = round( (1 - price/data['max']), 2)
        except ZeroDivisionError:
            data['prices'][index]['states']['weight'] = 0
    return data
