import aiohttp

from cocuvida.timehandle import timeofday, isodates
from cocuvida.sqldatabase import elspot as sql_elspot

from .api import API
from . import processelspot


class Application:
    URL = 'https://www.nordpoolgroup.com/api/marketdata/page/10'

    def __init__(self):
        self.url = self.URL
        self.status = None
        self.raw_data = None
        self.elspot_is_published_check = False

    async def on_startup(self):
        res = await sql_elspot.select_elspot_raw_data_for_date(isodates.today())
        if res == '':
            return
        res = await processelspot.reshape(res)
        for region in res:
            # INSERT INTO elspot_processed
            res = await sql_elspot.insert_processed_elspot(region)
            # PLOT BY DATE
            payload = await processelspot.plot_date(region)
            res = await sql_elspot.insert_plot_date(payload)
            # PLOT LIVE MARKER
            payload = await processelspot.plot_axvline_mark(region)
            res = await sql_elspot.insert_plot_live(payload)

    async def on_every_quarter(self):
        res = await sql_elspot.list_elspot_regions()
        for region in res:
            # PLOT LIVE MARKER
            res = await sql_elspot.select_processed_elspot_data_for_date(region, isodates.today())
            payload = await processelspot.plot_axvline_mark(res)
            res = await sql_elspot.insert_plot_live(payload)

    async def elspot_is_published(self) -> bool:
        '''
            returns True the first time we run this method after 13:30
            returns False in all other cases
        '''
        # if time now before 13:30
        if timeofday.is_before_time(13, 30):
            self.elspot_is_published_check = False
            return False
        # if we have already checked and time is after 13:30
        if self.elspot_is_published_check:
            return False
        # time is after 13:30 -> set elspot_is_published_check = True and return True
        self.elspot_is_published_check = True
        return True

    async def process_tomorrows_elspot(self) -> bool:
        '''
            download and convert elspot prices to reshaped and plots
        '''
        api = API()
        if await api.download():
            res = await processelspot.reshape(api.response_body)
            for region in res:
                payload = await processelspot.plot_date(region)
                res = await sql_elspot.insert_plot_date(payload)
                if not res:
                    self.elspot_is_published_check = False
                    return False
                # INSERT INTO elspot_processed
                res = await sql_elspot.insert_processed_elspot(region)
                if not res:
                    raise Exception('InsertError: table: elspot_processed', region['name'])

            return True
        self.elspot_is_published_check = False
