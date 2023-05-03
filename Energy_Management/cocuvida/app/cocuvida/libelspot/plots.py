from io import StringIO

import matplotlib.pyplot as plt
import numpy as np

from cocuvida.environment import env_ini_get
from cocuvida.timehandle import timeofday

Y_TICK_END_VAL = int(env_ini_get(section='cocuvida', key='elspot_plot_y_max'))
Y_TICK_STEP_VAL = int(env_ini_get(section='cocuvida', key='elspot_plot_y_step'))
Y_TICK_START_VAL = 0
Y_TICKS = [n for n in range(Y_TICK_START_VAL, Y_TICK_END_VAL+1, Y_TICK_STEP_VAL)]

PLOT_STYLE = 'dark_background'

COLOUR_YELLOW = '#FFFF6B'
COLOUR_APPLE_RED = '#FFAAAA'
COLOUR_LIGHT_RED = '#FFCCCC'
COLOUR_LIGHT_GREEN = '#BBFFBB'
COLOUR_ICE_BLUE = '#BBFFFF'


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
            use_colour = COLOUR_APPLE_RED
        elif price == int(elspot_region['min']):
            use_colour = COLOUR_ICE_BLUE
        elif price > int(elspot_region['average']):
            use_colour = COLOUR_LIGHT_RED
        elif price <= int(elspot_region['average']):
            use_colour = COLOUR_LIGHT_GREEN
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
    quarter_hour_now = timeofday.now_quarterhour()
    for index in value_index:
        price = int(elspot_region['prices'][index]['value'])
        if price == int(elspot_region['max']):
            use_colour = COLOUR_APPLE_RED
        elif price == int(elspot_region['min']):
            use_colour = COLOUR_ICE_BLUE
        elif price > int(elspot_region['average']):
            use_colour = COLOUR_LIGHT_RED
        elif price <= int(elspot_region['average']):
            use_colour = COLOUR_LIGHT_GREEN
        bars[index].set_width(0.7)
        bars[index].set_color(use_colour)
        time_start = elspot_region['prices'][index]['time_start']
        if time_start == quarter_hour_now:
            plt.axvline(x=(index+0.41), color=use_colour, alpha=0.6, lw=0.6)

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
