from cocuvida.timehandle import isodates, unix

from . import download, metadata, reshape, plots


class Elspot:
    '''
        this is an interface to simplify the interaction for this library
        you can however import parts of this library and call functions as you see fit
    '''
    # class variables
    live_plots = dict()

    def __init__(self):
        self.download_ok = False
        self.plot_ok = False
        self.process_ok = False

    async def download_dayahead(self, currency) -> str:
        '''
            returns the raw json received from the nordpool api endpoint
        '''
        self.download_ok = False
        response_text = await download.download_dayahead(currency)
        if response_text != '':
            self.download_ok = True
        return response_text

    async def process_dayahead(self, response_text: str) -> dict:
        '''
            after downloading, use this method to process the downloaded data
            loads response_text (a serialized json) into dict -> reshape -> add metadata
        '''
        self.process_ok = False
        processed = await reshape.reshape_dayahead(response_text)
        if processed != {}:
            for region, data in processed.items():
                processed[region] = await metadata.metadata_dayahead(data)
            self.process_ok = True
        return processed

    async def plot_dayahead_date(self, region_data: dict) -> str:
        '''
            pass one region from processed dayahead
            on success, returns an SVG string object with the plot
            on failure, returns empty string
        '''
        self.plot_ok = False
        plot = await plots.plot_dayahead_date(region_data)
        if plot != '':
            self.plot_ok = True
        return plot

    async def plot_dayahead_live(self, region_data: dict) -> str:
        '''
            pass one region from processed dayahead
            on success, returns an SVG string object with the plot
            on failure, returns empty string
        '''
        self.plot_ok = False
        plot = await plots.plot_dayahead_live(region_data)
        if plot != '':
            self.plot_ok = True
            region = region_data['region']
            # update class variable
            self.live_plots[region] = {'unix_timestamp': unix.timestamp(), 'plot': plot}
        return plot

    @classmethod
    async def get_plot_dayahead_live(cls, region: str) -> str:
        if region in cls.live_plots:
            unix_timestamp = cls.live_plots[region]['unix_timestamp']
            seconds_diff = unix.timestamp() - unix_timestamp
            if seconds_diff < 1000: # newer than 16-ish minutes means it is recent enough
                return cls.live_plots[region]['plot']
        return ''
