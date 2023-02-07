from pathlib import Path
import matplotlib.pyplot as plt
#import matplotlib.ticker as mticker
import numpy as np
import io
#from io import StringIO


class Plot:
    def __init__(self, envar_get: object):
        # data passed to generate plots will need to have this structure
        '''
        {
            'region':    'Molde,
            'currency':  'NOK',
            'date':      'YYYY-MM-DD',
            'unit':      'ore/kWh',
            'max':       '280',
            'min':       '143',
            'average':   '197',
            'resolution': 96,
            'prices': [
                {'index': 0,  'time_start': '00:00', 'time_end': '00:15', 'value': '210'},
                {'index': 1,  'time_start': '00:15', 'time_end': '00:30', 'value': '190'},
                {'index': 2,  'time_start': '00:30', 'time_end': '00:45', 'value': '200'},
                ..,
                ..,
                {'index': 94, 'time_start': '23:30', 'time_end': '00:45', 'value': '239'},
                {'index': 95, 'time_start': '23:45', 'time_end': '00:00', 'value': '247'}
            ]
        }
        '''
        start = int(envar_get('PLOT_Y_TICK_START'))
        end   = int(envar_get('PLOT_Y_TICK_END'))
        step  = int(envar_get('PLOT_Y_TICK_STEP'))
        self.generated_plots = []
        self.style = 'dark_background'
        self.y_ticks = [n for n in range(start, end+1, step)]
        self.bar_default_colour = '#559955'
        self.bar_select_colour = '#85C985'

        self.bar_max_colour = '#FFAAAA'
        self.bar_above_average_colour = '#FFCCCC'
        self.bar_below_average_colour = '#BBFFBB'
        self.bar_min_colour = '#BBFFFF'
        self.bar_first_in_step_colour = '#65B565'

        self.line_colour = '#559955'
        self.base_dir = '/home/elprice/bindmount/plots'


    def generate_bar_chart_bydate(self, data: dict) -> bool:
        self.payload = {}
        value_index = [x['index'] for x in data['prices']]
        try:
            plot_values = [int(x['value']) for x in data['prices']]
        except:
            # likely dataset without prices, for some regions this occur
            return False

        plt.style.use(self.style)
        _title = data['region'] + ' ' + data['date']
        plt.title(_title, y=1.0, pad=3, fontsize=14)
        plt.tight_layout()
        bars = plt.bar(value_index, plot_values, align='edge')
        for value in value_index:
            price = int(data['prices'][value]['value'])
            bars[value].set_width(0.7)
            if price == int(data['max']):
                bars[value].set_color(self.bar_max_colour)
            elif price == int(data['min']):
                bars[value].set_color(self.bar_min_colour)
            elif price >= int(data['average']):
                bars[value].set_color(self.bar_above_average_colour)
            elif price < int(data['average']):
                bars[value].set_color(self.bar_below_average_colour)

        plt.yticks(self.y_ticks)
        plt.xticks(fontsize=7, rotation=0)
        plt.grid(axis='y', alpha=0.3)

        # show ticks only for full hours instead of over-populating with each quarter
        x_ticks = [x['index'] for x in data['prices'] if x['time_start'][3:] == '00']
        hour_labels = [int(x['time_start'][0:2]) for x in data['prices'] if x['time_start'][3:] == '00']
        ax = plt.gca()
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(hour_labels)

        # plot_save_path = self.base_dir + '/bar/daily/' + data['date'] + '_' + data['region'] + '.svg'
        # Path(plot_save_path).parent.mkdir(parents=True, exist_ok=True) 
        # plt.savefig(plot_save_path, dpi=200)

        string_buffer = io.StringIO()
        plt.savefig(string_buffer, format='svg')
        string_buffer.seek(0)
        self.payload = { 
            'region': data['region'],
            'date': data['date'],
            'data': string_buffer.getvalue(),
        }
        string_buffer.close()

        plt.clf() # clear figure for next plot
        return True

    def generate_bar_chart_byhour(self, data: dict) -> bool:
        self.payload = []
        try:
            plot_values = [int(x['value']) for x in data['prices']]
            # using numpy.. for every hour, append the average between each 4 quarters
            plot_values = np.array(plot_values).reshape(-1, 4)
            plot_values = np.average(plot_values, axis=1)
        except:
            # likely dataset without prices, for some regions this occur
            return False

        # we are dealing with 24(23-25) hours, so the data must match
        value_index = [x for x in range(data['resolution']//4)] # -> [0, 1, 2,..., 23(22-24)]
        hour_labels = [int(x['time_start'][0:2]) for x in data['prices'] if x['time_start'][3:] == '00']


        # generate a total of 24(23-25 if daylight saving) plots, one for each hour of the day
        for index in value_index:
            title = data['region'] + ' ' + data['date'] + ' kl.' + str(hour_labels[index])
            plt.style.use(self.style)
            plt.title(title, y=1.0, pad=3, fontsize=14)
            plt.tight_layout()

            bars = plt.bar(value_index, plot_values, color=self.bar_default_colour, align='edge', width=0.9)
            bars[index].set_color(self.bar_select_colour)

            plt.yticks(self.y_ticks)
            plt.xticks(fontsize=7, rotation=0)
            plt.xticks(hour_labels)
            plt.grid(axis='y', alpha=0.3)

            # plot_save_path = self.base_dir + '/bar/hourly/' + data['region'] + '/' + data['date'] + '/' + 'index_' + str(hour_labels[index]) + '.svg'
            # Path(plot_save_path).parent.mkdir(parents=True, exist_ok=True) 
            # plt.savefig(plot_save_path, dpi=72)

            string_buffer = io.StringIO()
            plt.savefig(string_buffer, format='svg')
            string_buffer.seek(0)
            self.payload.append({
                'region': data['region'],
                'date': data['date'],
                'index':index,
                'hour': hour_labels[index],
                'data': string_buffer.getvalue(),
            })
            string_buffer.close()
            plt.clf()

        return True


    def generate_line_graph_bydate(self) -> bool:
        region = data['region']
        date = data['date']
        title = region + ' ' + date

        try:
            plot_values = [int(x['value']) for x in data['prices']]
            value_index = [x['index'] for x in data['prices']]
            has_prices = True
        except:
            # likely dataset without prices, for some regions this occur
            return False
        plt.style.use(self.style)
        plt.tight_layout()
        plt.title(title, y=1.0, pad=3, fontsize=14)

        plt.plot(value_index, plot_values, linewidth=1, color=self.line_colour)
        plt.yticks(self.y_ticks)
        plt.xticks(fontsize=7, rotation=0)
        plt.grid(axis='y', alpha=0.3)

        # fix only showing ticks for full hour, not every value/quarter
        x_ticks = [x['index'] for x in data['prices'] if x['time_start'][3:] == '00']
        hour_labels = [int(x['time_start'][0:2]) for x in data['prices'] if x['time_start'][3:] == '00']
        ax = plt.gca()
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(hour_labels)

        # plot_save_path = self.base_dir + '/line/daily/' + region + '.' + date + '.svg'
        # Path(plot_save_path).parent.mkdir(parents=True, exist_ok=True) 
        # plt.savefig(plot_save_path, dpi=200)

        string_buffer = io.StringIO()
        plt.savefig(string_buffer, format='svg')
        string_buffer.seek(0)
        self.payload = { 
            'region': data['region'],
            'date': data['date'],
            'data': string_buffer.getvalue(),
        }
        string_buffer.close()

        plt.clf() # clear figure for next plot
        return True
