import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
from cocuvida.timehandle import timeofday

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


async def plot_dayahead_date(elspot_region) -> str:
    value_index = [x['index'] for x in elspot_region['prices']]
    try:
        plot_values = [int(x['value']) for x in elspot_region['prices']]
    except:
        # likely dataset without prices, for some regions this occur
        return ''

    plt.style.use(PLOT_STYLE)
    title = elspot_region['region'] + ' ' + elspot_region['date'] + ' ' + elspot_region['unit']
    plt.title(title, y=1.0, pad=3, fontsize=14)
    plt.tight_layout()
    bars = plt.bar(value_index, plot_values, align='edge')
    for index in value_index:
        price = int(elspot_region['prices'][index]['value'])
        if price == int(elspot_region['max']):
            use_colour = BAR_MAX_COLOUR
        elif price == int(elspot_region['min']):
            use_colour = BAR_MIN_COLOUR
        elif price >= int(elspot_region['average']):
            use_colour = BAR_ABOVE_AVERAGE_COLOUR
        elif price < int(elspot_region['average']):
            use_colour = BAR_BELOW_AVERAGE_COLOUR
        bars[index].set_width(0.7)
        bars[index].set_color(use_colour)

    plt.yticks(Y_TICKS)
    plt.xticks(fontsize=7, rotation=0)
    plt.grid(axis='y', alpha=0.3)

    # show ticks only for full hours instead of over-populating with each quarter
    x_ticks = [x['index'] for x in elspot_region['prices'] if x['time_start'][3:] == '00']
    hour_labels = [int(x['time_start'][0:2]) for x in elspot_region['prices'] if x['time_start'][3:] == '00']
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


async def plot_dayahead_live(elspot_region) -> str:
    value_index = [x['index'] for x in elspot_region['prices']]
    try:
        plot_values = [int(x['value']) for x in elspot_region['prices']]
    except:
        # likely dataset without prices, for some regions this occur
        return ''

    plt.style.use(PLOT_STYLE)
    title = elspot_region['region'] + ' Now: ' + elspot_region['date'] + ' ' + elspot_region['unit']
    plt.title(title, y=1.0, pad=3, fontsize=14)
    plt.tight_layout()
    bars = plt.bar(value_index, plot_values, align='edge')
    vertical_line_inserted = False
    for index in value_index:
        price = int(elspot_region['prices'][index]['value'])
        if price == int(elspot_region['max']):
            use_colour = BAR_MAX_COLOUR
        elif price == int(elspot_region['min']):
            use_colour = BAR_MIN_COLOUR
        elif price >= int(elspot_region['average']):
            use_colour = BAR_ABOVE_AVERAGE_COLOUR
        elif price < int(elspot_region['average']):
            use_colour = BAR_BELOW_AVERAGE_COLOUR
        bars[index].set_width(0.7)
        bars[index].set_color(use_colour)
        time_start = elspot_region['prices'][index]['time_start']
        h = int(time_start[:2])
        m = int(time_start[3:])
        if timeofday.is_before_time(h,m):
            if not vertical_line_inserted:
                plt.axvline(x=(index-0.6), color=use_colour, alpha=0.6, lw=0.6)
                vertical_line_inserted = True

    plt.yticks(Y_TICKS)
    plt.xticks(fontsize=7, rotation=0)
    plt.grid(axis='y', alpha=0.3)

    # show ticks only for full hours instead of over-populating with each quarter
    x_ticks = [x['index'] for x in elspot_region['prices'] if x['time_start'][3:] == '00']
    hour_labels = [int(x['time_start'][0:2]) for x in elspot_region['prices'] if x['time_start'][3:] == '00']
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
