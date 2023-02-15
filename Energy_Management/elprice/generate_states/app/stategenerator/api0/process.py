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
