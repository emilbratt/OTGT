from .const import COLOURS


def overview(reshaped_region: dict) -> None:
    print(f'---Overview---')
    print('Date:'.ljust(13),str(reshaped_region['date']))
    print('Currency:'.ljust(13),str(reshaped_region['currency']))
    print('Unit:'.ljust(13),str(reshaped_region['unit']))
    print('Max:'.ljust(13),str(reshaped_region['max']))
    print('Min:'.ljust(13),str(reshaped_region['min']))
    print('Average:'.ljust(13),str(reshaped_region['average']))
    print('Resolution:'.ljust(13),str(reshaped_region['resolution']))
    _max = reshaped_region['max']
    justify = len(str(_max)) + 10
    price_strings = []
    line_break = str()
    create_line_break = True
    for entry in reshaped_region['prices']:
        time_start = entry['time_start']
        minute = time_start[3:]
        hour = time_start[:2]
        price = entry['value']
        if minute == '00':
            price_hour_string = f'|  Hour {hour}  '
        price_hour_string += f'|{str(price).center(justify)}'
        if minute == '45':
            price_hour_string += '|'
            price_strings.append(price_hour_string)
            if create_line_break:
                create_line_break = False
                for _ in price_hour_string:
                    line_break += '-'
    print(line_break)
    print('Prices')
    print(line_break)
    for string in price_strings:
        print(string)
    print(line_break)
    print()


def vertical_curve(reshaped_region: dict) -> None:
    p_desc = 'Percent Bar'.ljust(99)
    print(f'Time  | {p_desc}|')
    _min = reshaped_region['min']
    _max = reshaped_region['max']
    price_diff = _max-_min
    for entry in reshaped_region['prices']:
        time_start = entry['time_start']
        price = entry['value']
        percent = round((price-_min) * (100 / (price_diff)))
        if percent > 80:
            colour = COLOURS['red']
        elif percent > 60:
            colour = COLOURS['yellow']
        elif percent > 40:
            colour = COLOURS['purple']
        elif percent > 20:
            colour = COLOURS['green']
        else:
            colour = COLOURS['aqua']
        bar = '|' + colour
        for i in range(percent):
            bar += 'o'
        for i in range(100-percent):
            bar += '.'
        bar += COLOURS['default'] + '|'
        print(f'{time_start} {bar}')
    print()

def horizontal_curve(reshaped_region: dict) -> None:
    rows = []
    hour_string_row = str()
    _max = reshaped_region['max']
    _min = reshaped_region['min']
    price_diff = _max-_min
    for entry in reshaped_region['prices']:
        time_start = entry['time_start']
        minute = time_start[3:]
        hour = time_start[:2]
        price = entry['value']
        try:
            p = round( (price-_min) * (100 / price_diff) )
        except ZeroDivisionError:
            p = 100
        rows.append(p)
        if minute == '00':
            hour_string_row += hour.ljust(4)
    x_desc = f' time |{hour_string_row}|'
    for i in range(101, -1, -5):
        y_desc = f'{str(i-1)} %'.rjust(5)
        bar = f'{y_desc} |'
        for p in rows:
            if p > 80:
                colour = COLOURS['red']
            elif p > 60:
                colour = COLOURS['yellow']
            elif p > 40:
                colour = COLOURS['purple']
            elif p > 20:
                colour = COLOURS['green']
            else:
                colour = COLOURS['aqua']

            if p >= i:
                bar += colour + '|'
            elif p < i-5:
                bar += '-'
            else:
                bar += colour + 'o'
            bar += COLOURS['default']
        bar += '|'
        print(bar)
    print(x_desc)
    print()
