import matplotlib.pyplot as plt
import numpy as np
from io import StringIO

Y_TICK_START_VAL = 0
Y_TICK_END_VAL   = 800
Y_TICK_STEP_VAL  = 50
Y_TICKS = [n for n in range(Y_TICK_START_VAL, Y_TICK_END_VAL+1, Y_TICK_STEP_VAL)]

PLOT_STYLE = 'dark_background'
BAR_DEFAULT_COLOUR = '#559955'
BAR_SELECT_COLOUR = '#85C985'

BAR_MAX_COLOUR = '#FFAAAA'
BAR_ABOVE_AVERAGE_COLOUR = '#FFCCCC'
BAR_BELOW_AVERAGE_COLOUR = '#BBFFBB'
BAR_MIN_COLOUR = '#BBFFFF'
BAR_FIRST_IN_STEP_COLOUR = '#65B565'

LINE_COLOUR = '#559955'


async def plot_date(elspot_data) -> str:
    plot = str()
    value_index = [x['index'] for x in elspot_data['prices']]
    try:
        plot_values = [int(x['value']) for x in elspot_data['prices']]
    except:
        # likely dataset without prices, for some regions this occur
        return plot

    plt.style.use(PLOT_STYLE)
    title = elspot_data['region'] + ' ' + elspot_data['date']
    plt.title(title, y=1.0, pad=3, fontsize=14)
    plt.tight_layout()
    bars = plt.bar(value_index, plot_values, align='edge')
    for value in value_index:
        price = int(elspot_data['prices'][value]['value'])
        bars[value].set_width(0.7)
        if price == int(elspot_data['max']):
            bars[value].set_color(BAR_MAX_COLOUR)
        elif price == int(elspot_data['min']):
            bars[value].set_color(BAR_MIN_COLOUR)
        elif price >= int(elspot_data['average']):
            bars[value].set_color(BAR_ABOVE_AVERAGE_COLOUR)
        elif price < int(elspot_data['average']):
            bars[value].set_color(BAR_BELOW_AVERAGE_COLOUR)

    plt.yticks(Y_TICKS)
    plt.xticks(fontsize=7, rotation=0)
    plt.grid(axis='y', alpha=0.3)

    # show ticks only for full hours instead of over-populating with each quarter
    x_ticks = [x['index'] for x in elspot_data['prices'] if x['time_start'][3:] == '00']
    hour_labels = [int(x['time_start'][0:2]) for x in elspot_data['prices'] if x['time_start'][3:] == '00']
    ax = plt.gca()
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(hour_labels)

    string_buffer = StringIO()
    plt.savefig(string_buffer, format='svg')
    string_buffer.write('<!--title: ' + title + '-->' + '\n')
    string_buffer.seek(0)
    plot = string_buffer.getvalue()
    string_buffer.close()
    # clear figure for next plot
    plt.clf()
    return plot
