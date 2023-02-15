def check(data: dict):
    # if all the values are cast-able to int, we are golden
    try:
        prices_value = [int(x['value']) for x in data['prices']]
        return True
    except:
        # likely dataset without prices, for some regions this occur
        return False


def percent(data: dict):
    '''
        lower percentage = better
        min price = 0%
        max price = 100%

        all other prices will have a value between 0% and 100%

        if we have many prices < 50%
            this means we have price spikes in the higher range (pyramid curve)
            results in a longer period of below average prices and few very hight prices

        if we have many prices > 50%
            this means we have price spikes in the lower range (valley curve)
            results in a longer period of above average prices and few very low prices

        if we have many prices split apart (e.g. < 30% and > 70%)
            this means that prices vary alot throughout the day
            results in higher fluctuation between high and low prices
    '''
    for index in range(data['resolution']):
        price = data['prices'][index]['value']
        percent = (price-data['min']) * (100 / (data['max']-data['min']))
        data['prices'][index]['percent'] = int(percent)
    return data


def diff_factor(data: dict):
    '''
        lower diff_factor = better
        ranges from: 1
        min price = 1

        if price = 750 and min = 250 -> diff_factor = 3
            higher diff_factor means a higher difference between this and the lowest price

        if the highest price has a diff_factor = 4
            that means the highest price is 4 times higher than the lowest price
    '''
    for index in range(data['resolution']):
        price = data['prices'][index]['value']
        data['prices'][index]['diff_factor'] = round(price/data['min'], 2)
    return data


def weight(data: dict):
    '''
        higher weight = better
        ranges from: 0 to approaching 1
        max price = 0

        the further from 0 (approaching 1) the more inclined you would be to turn on device
        if weight = 0
            this means that the price is 1/1 of max price
        if weight = 0.25
            this means that the price is 3/4 of max price
        if weight = 0.33
            this means that the price is 2/3 of max price
        if weight = 0.5
            this means that the price is 2/4 of max price
        if weight = 0.66
            this means that the price is 1/3 of max price
        if weight = 0.75
            this means that the price is 1/4 of max price

        ..basically as weight appriaches 1, the price is further away from max price
    '''
    for index in range(data['resolution']):
        price = data['prices'][index]['value']
        weight = round( (1 - price/data['max']), 2)
        data['prices'][index]['weight'] = round( (1 - price/data['max']), 2)
    return data


if __name__ == '__main__':
    from os import path
    import json

    with open('./test_data/elspot/reshaped_2023-01-23.json', 'r') as my_file:
        for region in json.load(my_file):
            data = region
            if data['region'] == 'Molde':
                if check(data):
                    data = percent(data)
                    data = diff_factor(data)
                    data = weight(data)
                    for row in data['prices']:
                        print('index',row['index'], 'value', row['value'], 'percent', row['percent'], 'diff_factor', round(row['diff_factor'], 2), 'weight', row['weight'])
                        print('-')
