import random
from statistics import mean
from datetime import datetime, timedelta

class Generate:

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

    def __init__(self):
        # data object for calculating dates and times etc.
        self.date_object = datetime.fromisoformat('1999-01-01T00:00:00')
        # the structure of the data
        self.data = {
            'region': 'Region',
            'date': '1999-01-01',
            'currency': 'NOK',
            'unit': 'ore/kWh',
            'max': None,
            'min': None,
            'average': None,
            'resolution': 24,
            'prices': [],
        }
        # the parameters for generating prices
        self.parameters = {
            'from_val' : 10,
            'to_val' : 100,
            'split_hours': 1,
            'fluctuate_level' : 0,
            'spike_level' : 1,
            'dip_level' : 1,
            'sort_prices' : False,
            'sort_offset_factor' : 1,
        }
        self.is_initialized = False
        self.is_generated = False

    def set_date(self, isodate: str):
        self.date_object = datetime.fromisoformat(isodate)

    def set_region(self, region: str):
        self.data['region'] = region

    def split_hours(self, n=1):
        if n not in self.VALID_SPLIT_MINUTES:
            print('use on of these', self.VALID_SPLIT_MINUTES)
            exit(1)
        self.parameters['split_hours'] = n
        self.data['resolution'] = n*24

    def from_val(self, n: int):
        self.parameters['from_val'] = n

    def to_val(self, n: int):
        self.parameters['to_val'] = n

    def fluctuate_level(self, n: int):
        if n > 10:
            n = 10
        self.parameters['fluctuate_level'] = n

    def spike_level(self, n: int):
        if n > 10:
            n = 10
        self.parameters['spike_level'] = n

    def dip_level(self, n: int):
        if n > 10:
            n = 10
        self.parameters['dip_level'] = n

    def sort_prices(self, _bool=True):
        self.parameters['sort_prices'] = _bool

    def sort_offset_factor(self, n: int):
        self.parameters['sort_offset_factor'] = n

    def initialize(self):
        # empty prices (might have been populated by a previous run)
        self.data['prices'] = []
        minute_mark = 60 // (self.data['resolution'] // 24)
        minutes_splits = [f*minute_mark for f in range((self.data['resolution'] // 24))]
        index = 0
        for hour in range(24):
            for minute in minutes_splits:
                t_start = self.date_object + timedelta(hours=hour, minutes=minute)
                t_end   = self.date_object + timedelta(hours=hour, minutes=(minute+minute_mark))
                row = {
                    'index':index,
                    'time_start': t_start.strftime('%H:%M'),
                    'time_end': t_end.strftime('%H:%M'),
                    'value': None,
                }
                self.data['prices'].append(row)
                index += 1
        self.data['resolution'] = index
        self.is_initialized = True

    def generate_prices(self) -> dict:
        if not self.is_initialized:
            print('run method initialize() first')
            exit(1)
        from_val = self.parameters['from_val']
        to_val = self.parameters['to_val']
        fluctuate_level = self.parameters['fluctuate_level']
        spike_level = self.parameters['spike_level']
        dip_level = self.parameters['dip_level']

        # add random prices
        prices = []
        for index in range(self.data['resolution']):
            prices.append(random.randint(from_val, to_val))

        # fluctuate prices
        if fluctuate_level > 0:
            temp_prices = []
            middle = (to_val + from_val) // 2
            for price in prices:
                if price <= middle:
                    new_price = price // 2
                else:
                    new_price = price + (to_val - price) // 2
                if random.randint(0, fluctuate_level) == 1:
                    new_price = price
                temp_prices.append(new_price)
                prices = temp_prices

        # spike prices
        if spike_level > 0:
            temp_prices = []
            middle = (to_val + from_val) // 2
            for price in prices:
                new_price = price
                if price > middle:
                    new_price = random.randint(from_val, middle) 
                    if random.randint(0, spike_level) == 1:
                        new_price = price
                temp_prices.append(new_price)
            prices = temp_prices

        # spike prices
        if dip_level > 0:
            temp_prices = []
            middle = (to_val + from_val) // 2
            for price in prices:
                new_price = price
                if price <= middle:
                    new_price = random.randint(middle, to_val) 
                    if random.randint(0, dip_level) == 1:
                        new_price = price
                temp_prices.append(new_price)
            prices = temp_prices

        if not self.parameters['sort_prices']:
            random.shuffle(prices)
        elif self.parameters['sort_prices']:
            prices.sort()
            sort_offset_factor = self.parameters['sort_offset_factor']
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

        self.price_list = prices
        self.data['max']     = max(prices)
        self.data['min']     = min(prices)
        self.data['average'] = round(mean(prices))
        for index in range(self.data['resolution']):
            self.data['prices'][index]['value'] = prices[index]
        self.is_generated = True
        return self.data

    def get_price_list(self):
        return self.price_list

    def print_data(self):
        if not self.is_generated:
            print('run method generate_prices() first')
            exit(1)
        print('Region:'.ljust(13),str(self.data['region']))
        print('Date:'.ljust(13),str(self.data['date']))
        print('Currency:'.ljust(13),str(self.data['currency']))
        print('Unit:'.ljust(13),str(self.data['unit']))
        print('Max:'.ljust(13),str(self.data['max']))
        print('Min:'.ljust(13),str(self.data['min']))
        print('Average:'.ljust(13),str(self.data['average']))
        print('Resolution:'.ljust(13),str(self.data['resolution']))
        print('Fluctuat_level:'.ljust(13),str(self.parameters['fluctuate_level']))
        print('Prices from', str(self.parameters['from_val']), 'to', str(self.parameters['to_val']))
        for hour in range(24):
            s = hour * self.parameters['split_hours']
            e = hour * self.parameters['split_hours'] + self.parameters['split_hours']
            batch = self.price_list[s:e]
            print('hour', str(hour).ljust(2), '->', batch)

    def print_vertical_price_curve(self):
        if not self.is_generated:
            print('run method generate_prices() first')
            exit(1)
        for price in self.price_list:
            percent = round( (price-self.data['min']) * (100 / (self.data['max']-self.data['min'])) )
            if percent > 80:
                colour = self.COLOURS['aqua']
            elif percent > 60:
                colour = self.COLOURS['green']
            elif percent > 40:
                colour = self.COLOURS['purple']
            elif percent > 20:
                colour = self.COLOURS['yellow']
            else:
                colour = self.COLOURS['red']
            bar = '|' + colour
            for i in range(percent):
                bar += 'o'
            for i in range(100-percent):
                bar += '.'
            bar += self.COLOURS['default'] + '|'
            print(bar)

    def print_horizontal_price_curve(self):
        if not self.is_generated:
            print('run method generate_prices() first')
            exit(1)
        percentages = []
        price_diff = self.data['max']-self.data['min']
        for price in self.price_list:
            p = round( (price-self.data['min']) * (100 / price_diff) )
            percentages.append(p)

        for i in range(101, -1, -5):
            bar = ''
            for p in percentages:
                # set colouor
                if p > 80:
                    bar += self.COLOURS['aqua']
                elif p > 60:
                    bar += self.COLOURS['green']
                elif p > 40:
                    bar += self.COLOURS['purple']
                elif p > 20:
                    bar += self.COLOURS['yellow']
                else:
                    bar += self.COLOURS['red']

                # add symbol
                if p >= i:
                    bar += '|'
                elif p < i-5:
                    bar += ' '
                else:
                    bar += 'o'
                bar += self.COLOURS['default']
            print(bar)


# showcase how to use if running this script directly
if __name__ == '__main__':
    gnrt = Generate()
    # these must be set
    gnrt.from_val(10) # min value to include
    gnrt.to_val(1000) # max value to include

    # these can be omitted
    gnrt.fluctuate_level(0) # 0 - 10
    gnrt.spike_level(0) # 0 - 10
    gnrt.dip_level(0) # 0 - 10
    gnrt.set_date('2000-01-01') # pass iso 6801 string
    gnrt.set_region('Oslo') # set name of region
    gnrt.split_hours(4) # split hour into 2 or 4
    gnrt.sort_prices() # sort prices
    gnrt.sort_offset_factor(7) # 0 - X offsets the sorted prices

    # generate prices
    gnrt.initialize() # must be called before generating
    data = gnrt.generate_prices() # generates the data, do whatever you want with it
    price_list = gnrt.get_price_list() # returns only the prices as an array

    # print out info
    gnrt.print_data() # prints metadata
    gnrt.print_vertical_price_curve() # prints price curve top-to-bottom
    gnrt.print_horizontal_price_curve() # prints price curve left-to-right
