from os import path
import json
import random
from statistics import mean

COLOURS = {
    'green': '\033[92m',
    'blue': '\033[94m',
    'red': '\033[31m',
    'brown': '\033[33m',
    'purple': '\033[95m',
    'default': '\033[0m',
    'aqua': '\033[96m',
    'yellow': '\033[93m',
}


class DummyData:
    def __init__(self):
        self.template_file = './test_data/elspot/template.json'

    def generate_prices(self, val_from=10, val_to=100, fluctuate=False, high_spike=False, low_spike=False, sort_prices=False, sort_offset_factor=1) -> dict:
        self.fluctuate = fluctuate
        self.val_from = val_from
        self.val_to = val_to
        with open(self.template_file, 'r') as open_file:
            self.data = json.load(open_file)

        # fluctuate = True will force prices closer to min and max value
        diff = val_to - val_from
        fluct_max_lim = val_to - (diff // 1)
        fluct_min_lim = val_from + (diff // 1)
        if fluctuate:
            fluct_max_lim = val_to - (diff // 5)
            fluct_min_lim = val_from + (diff // 5)
        if high_spike:
            fluct_max_lim = val_to - (diff // 10)
        if low_spike:
            fluct_min_lim = val_from + (diff // 10)
        # populate prices

        prices = []
        for index in range(self.data['resolution']):
            not_fluctuating = True
            while not_fluctuating:
                value = random.randint(val_from, val_to)
                rng = random.randint(1,10)
                if high_spike and not low_spike:
                    if rng <= 8 and value < fluct_min_lim:
                        not_fluctuating = False
                    elif rng <= 2 and value > fluct_max_lim:
                        not_fluctuating = False
                elif low_spike and not high_spike:
                    if rng <= 8 and value > fluct_max_lim:
                        not_fluctuating = False
                    elif rng <= 2 and value < fluct_min_lim:
                        not_fluctuating = False
                elif low_spike and high_spike:
                    if value < fluct_min_lim or value > fluct_max_lim:
                        not_fluctuating = False
                elif not low_spike and not high_spike:
                    if value < fluct_min_lim or value > fluct_max_lim or rng >= 8:
                        not_fluctuating = False

            prices.append(value)

        if sort_prices:
            prices.sort()
            offset_factor = 5
            offset = self.data['resolution'] // sort_offset_factor
            offset_list = []
            for i in range(offset, self.data['resolution']+offset):
                if i >= self.data['resolution']:
                    j = i - self.data['resolution']
                else:
                    j = i
                offset_list.append(prices[j])
            prices = offset_list

        for index in range(self.data['resolution']):
            self.data['prices'][index]['value'] = prices[index]
        # create a quick list to do calculations for avg, min and max
        price_list = [x['value'] for x in self.data['prices']]
        self.data['max']     = max(price_list)
        self.data['min']     = min(price_list)
        self.data['average'] = mean(price_list)
        return self.data


    def print_prices(self):
        print('GENERATED PRICES')
        print('fluctuate', self.fluctuate)
        print('val from', self.val_from)
        print('val to', self.val_to)
        print('price list')
        print([x['value'] for x in self.data['prices']])
        print('-')
        print('average', int(self.data['average']))
        print('max', self.data['max'])
        print('min', self.data['min'])



def check(data: dict):
    # if all the values are cast-able to int, we are golden
    try:
        prices_value = [int(x['value']) for x in data['prices']]
    except:
        # likely dataset without prices, for some regions this occur
        return False
    for index in range(data['resolution']):
        if data['prices'][index]['index'] != index:
            print(index)
            return False
    return True

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


def spike_level(data: dict) -> dict:
    '''
        high fluctuation and difference between low and max
        with few in-between will increase the spike level

        leels
            level 1 -> no spike
            level 2 -> small spike
            level 3 -> noticable spike
            level 4 -> serious spike
            level 5 -> critical spike
        ]
    '''
    spike_levels = [
        {'step': 0, 'level': 1},
        {'step': 80, 'level': 2},
        {'step': 100, 'level': 3},
        {'step': 120, 'level': 4},
        {'step': 150, 'level': 5},
    ]
    percent = 0
    weight = 0
    diff_factor = 0
    for index in range(data['resolution']):
        percent += data['prices'][index]['states']['percent']
        weight +=  data['prices'][index]['states']['weight']
        diff_factor += data['prices'][index]['states']['diff_factor']
    percent = int(percent/data['resolution'])
    weight  = int((weight/data['resolution'] * 200))
    diff_factor = int((diff_factor/data['resolution']) * 10)
    spike_level = percent + weight + diff_factor

    # print('percent', percent)
    # print('weight', weight)
    # print('diff_factor', diff_factor)
    # print('spike_level', spike_level)
    # exit()
    data['states']['spike_level'] = spike_level
    for row in spike_levels:
        if spike_level > row['step']:
            data['states']['spike_level'] = row['level']
    return data


def print_result_after_states(data):
    print('GENERATED STATES')
    for row in data['prices']:
        p = row['states']['percent']
        if p < 20:
            colour = COLOURS['aqua']
        elif p < 35:
             colour = COLOURS['green']
        elif p > 80:
            colour = COLOURS['red']
        elif p > 65:
            colour = COLOURS['purple']
        else:
            colour = COLOURS['yellow']
        print(
            colour,
            'index',row['index'], '  ',
            'value', row['value'], '  ',
            'percent', row['states']['percent'], '  ',
            'diff_factor', row['states']['diff_factor'], '  ',
            'weight', row['states']['weight']
        )
    print(COLOURS['default'] + '--')
    print('spike_level', data['states']['spike_level'])
if __name__ == '__main__':

    dum = DummyData()
    data = dum.generate_prices(val_from=-40, val_to=250, fluctuate=True, high_spike=True, low_spike=False, sort_prices=True, sort_offset_factor=5)
    data = dum.generate_prices(val_from=40, val_to=150, fluctuate=True, high_spike=False, low_spike=True, sort_prices=True, sort_offset_factor=5)
    data = dum.generate_prices(val_from=40, val_to=150, fluctuate=True, high_spike=True, low_spike=False, sort_prices=True, sort_offset_factor=5)
    data = dum.generate_prices(val_from=80, val_to=150, fluctuate=False, high_spike=True, low_spike=False, sort_prices=True, sort_offset_factor=5)
    #data = dum.generate_prices(val_from=120, val_to=150, fluctuate=False, high_spike=False, low_spike=False, sort_prices=True, sort_offset_factor=5)
    dum.print_prices()
    data['states'] = {}
    for index in range(data['resolution']):
        data['prices'][index]['states'] = {}
    print('.')
    data = percent(data)
    data = diff_factor(data)
    data = weight(data)
    data = spike_level(data)
    print_result_after_states(data)

    exit()

    test_file = './test_data/elspot/reshaped_2023-01-23.json'

    with open(test_file, 'r') as my_file:
        for region in json.load(my_file):
            data = region
            if data['region'] == 'Molde':
                if check(data):
                    for index in range(data['resolution']):
                        data['prices'][index]['states'] = {}
                    data = percent(data)
                    data = diff_factor(data)
                    data = weight(data)
                    print_result_after_states(data)
