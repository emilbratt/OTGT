def check(data: dict):
    # if all the values are cast-able to int, we are golden
    try:
        prices_value = [int(x['value']) for x in data['prices']]
        return True
    except:
        # likely dataset without prices, for some regions this occur
        return False

def percent(data: dict):
    # this function adds the "precent" key to the prices list
    # ranging from 0 to 100 where 100 = max price, 0 = lowest price
    '''
    from

        'prices': [
            {'index': 0,  'time_start': '00:00', 'time_end': '00:15', 'value': '210'},

    to
        'prices': [
            {'index': 0,  'time_start': '00:00', 'time_end': '00:15', 'value': '210', 'percent': 30},
    '''
    for index in range(data['resolution']):
        price = data['prices'][index]['value']
        percent = ( (price-data['min']) * (100 / (data['max']-data['min'])) )
        data['prices'][index]['percent'] = int(percent)
    return data
