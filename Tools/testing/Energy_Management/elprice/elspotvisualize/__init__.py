VALID_SPLIT_MINUTES = [1,2,4]
COLOURS = {
    'default': '\033[0m',
    'green': '\033[92m',
    'blue': '\033[94m',
    'red': '\033[31m',
    'brown': '\033[33m',
    'purple': '\033[95m',
    'aqua': '\033[96m',
    'yellow': '\033[93m',
}

def reshaped_overview(data_reshaped: dict):
    print('Region:'.ljust(13),str(data_reshaped['region']))
    print('Date:'.ljust(13),str(data_reshaped['date']))
    print('Currency:'.ljust(13),str(data_reshaped['currency']))
    print('Unit:'.ljust(13),str(data_reshaped['unit']))
    print('Max:'.ljust(13),str(data_reshaped['max']))
    print('Min:'.ljust(13),str(data_reshaped['min']))
    print('Average:'.ljust(13),str(data_reshaped['average']))
    print('Resolution:'.ljust(13),str(data_reshaped['resolution']))
    batch_count = 0
    data_reshaped['prices'][0]['time_end'][3:]
    keep_adding = True
    while keep_adding:
        if data_reshaped['prices'][batch_count]['time_end'][3:] == '00':
            keep_adding = False
        batch_count += 1
    price_list = [x['value'] for x in data_reshaped['prices']]
    for hour in range(data_reshaped['resolution']//batch_count):
        price_string = 'From ' + str(hour).rjust(2) + ':'
        s = hour * batch_count
        e = hour * batch_count + batch_count
        batch = price_list[s:e]
        for price in batch:
            price_string += str(price).rjust(len(str(data_reshaped['max']))+ 3)
        print(price_string)

def reshaped_vertical_curve(data_reshaped: dict):
    price_list = [x['value'] for x in data_reshaped['prices']]
    for price in price_list:
        percent = round( (price-data_reshaped['min']) * (100 / (data_reshaped['max']-data_reshaped['min'])) )
        if percent > 80:
            colour = COLOURS['aqua']
        elif percent > 60:
            colour = COLOURS['green']
        elif percent > 40:
            colour = COLOURS['purple']
        elif percent > 20:
            colour = COLOURS['yellow']
        else:
            colour = COLOURS['red']
        bar = '|' + colour
        for i in range(percent):
            bar += 'o'
        for i in range(100-percent):
            bar += '.'
        bar += COLOURS['default'] + '|'
        print(bar)

def reshaped_horizontal_curve(data_reshaped: dict):
    price_diff = data_reshaped['max']-data_reshaped['min']
    price_list = [x['value'] for x in data_reshaped['prices']]
    percentages = []
    for price in price_list:
        try:
            p = round( (price-data_reshaped['min']) * (100 / price_diff) )
        except ZeroDivisionError:
            p = 100
        percentages.append(p)

    for i in range(101, -1, -5):
        bar = ''
        for p in percentages:
            # set colouor
            if p > 80:
                bar += COLOURS['aqua']
            elif p > 60:
                bar += COLOURS['green']
            elif p > 40:
                bar += COLOURS['purple']
            elif p > 20:
                bar += COLOURS['yellow']
            else:
                bar += COLOURS['red']

            # add symbol
            if p >= i:
                bar += '|'
            elif p < i-5:
                bar += ' '
            else:
                bar += 'o'
            bar += COLOURS['default']
        print(bar)


def horizontal_curve(arr: list) -> str:
    colour = COLOURS['red']

    _min_ = min(arr)
    _max_ = max(arr)
    diff = _max_ - _min_

    percentages = []
    for val in arr:
        try:
            p = round( (val-_min_) * (100 / diff) )
        except ZeroDivisionError:
            p = 100
        percentages.append(p)

    for i in range(101, -1, -5):
        bar = ''
        for p in percentages:
            # set colouor
            if p > 80:
                bar += COLOURS['aqua']
            elif p > 60:
                bar += COLOURS['green']
            elif p > 40:
                bar += COLOURS['purple']
            elif p > 20:
                bar += COLOURS['yellow']
            else:
                bar += COLOURS['red']

            # add symbol
            if p >= i:
                bar += '|'
            elif p < i-5:
                bar += ' '
            else:
                bar += 'o'
            bar += COLOURS['default']
        print(bar)

def percent_bar(_cur: int, _min: int, _max: int) -> str:
    diff = _max - _min
    p = round( (_cur-_min) * (100 / diff) )

    colour = COLOURS['red']
    if p > 80:
        colour = COLOURS['aqua']
    elif p > 60:
        colour = COLOURS['green']
    elif p > 40:
        colour = COLOURS['purple']
    elif p > 20:
        colour = COLOURS['yellow']
    else:
        colour = COLOURS['red']
    base = '|' + colour
    for i in range(p):
        base += 'o'
    for i in range(100-p):
        base += '.'
    base += COLOURS['default'] + '|'
    print(base)
