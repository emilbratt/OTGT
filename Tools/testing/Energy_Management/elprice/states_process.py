def check(data: dict):
    # if all the values are cast-able to int, we are golden
    try:
        prices_value = [int(x['value']) for x in data['prices']]
        return True
    except:
        # likely dataset without prices, for some regions this occur
        return False


def percent(data: dict):
    max_price    = data['max']
    min_price    = data['min']
    for index in range(data['resolution']):
        price = data['prices'][index]['value']
        percent = ( (price-min_price) * (100 / (max_price-min_price)) )
        data['prices'][index]['percent'] = int(percent)
    return data



if __name__ == '__main__':
    from os import path
    import json

    with open('./test_data/elspot/reshaped_2023-01-23.json', 'r') as my_file:
        data = json.load(my_file)
        for region in data:
            if check(region):
                new_data = percent(region)
                for row in new_data['prices']:
                    print('index',row['index'])
                    print('time', row['time_start'])
                    print('value', row['value'])
                    print('percent', row['percent'])
                    print('-')
