from cocuvida.timehandle import timeofday, isodates
from cocuvida.sqldatabase import elspot as sql_elspot

from .api import API
from . import processelspot


# FIXME: remove all SQL related code (simple decoupling) and put SQL related code into the Elspot service instead
class Elspot:

    def __init__(self):
        self.elspot_tomorrow_check = False

    async def on_startup(self) -> bool:
        # DOWNLOAD ELSPOT (if startup is before 13:00 we get todays, else we get tomorrows)
        downloaded_todays = False
        downloaded_tomorrows = False
        api = API()
        is_downloaded = await api.download_elspot()
        if is_downloaded:
            res = await processelspot.reshape(api.response_body)
            if res == []:
                print('ELSPOT: reshape failed')
                return False
            # grab date from inside the first region in the reshaped elspot data
            downloaded_date = res[0]['date']
            if downloaded_date == isodates.today_plus_days(1):
                downloaded_tomorrows = True
                downloaded_todays = False
            elif downloaded_date == isodates.today():
                downloaded_todays = True
                downloaded_tomorrows = False
            for region in res:
                # ADD METADATA
                region_with_metadata = await processelspot.add_metadata(region)
                # INSERT INTO elspot_processed
                res = await sql_elspot.insert_processed_elspot(region_with_metadata)
                if not res:
                    raise Exception('InsertError: error inserting processed_elspot into SQL table "elspot_processed"')
                # GENERATE PLOT BY DATE
                payload = await processelspot.plot_date(region_with_metadata)
                res = await sql_elspot.insert_plot_date(payload)
                # extra steps if todays where downloaded
                if downloaded_todays:
                    # GENERATE PLOT WITH TIME MARKER
                    payload = await processelspot.plot_axvline_mark(region_with_metadata)
                    res = await sql_elspot.insert_plot_live(payload)

        if downloaded_todays:
            self.elspot_tomorrow_check = False
            # nothing more to do
            return True
        elif downloaded_tomorrows:
            # set tomorrow check true so that we do not need to do this again when mainloop is entered
            self.elspot_tomorrow_check = True
            # hanlde todays elspot prices (if exist in database)
            res = await sql_elspot.select_elspot_raw_data_for_date(isodates.today())
            if res == '':
                # raw elspot prices does not exist in database, nothing more to do
                return True
            res = await processelspot.reshape(res)
            for region in res:
                # ADD METADATA
                region_with_metadata = await processelspot.add_metadata(region)
                # INSERT INTO elspot_processed
                res = await sql_elspot.insert_processed_elspot(region_with_metadata)
                # GENERATE PLOT BY DATE
                payload = await processelspot.plot_date(region_with_metadata)
                res = await sql_elspot.insert_plot_date(payload)
                # GENERATE PLOT WITH TIME MARKER
                payload = await processelspot.plot_axvline_mark(region_with_metadata)
                res = await sql_elspot.insert_plot_live(payload)
            return True

        return False

    async def generate_live_plots(self):
        res = await sql_elspot.list_elspot_regions()
        for region in res:
            # PLOT LIVE MARKER
            res = await sql_elspot.select_processed_elspot_data_for_date(region, isodates.today())
            if res != {}:
                payload = await processelspot.plot_axvline_mark(res)
                res = await sql_elspot.insert_plot_live(payload)

    async def elspot_is_published(self) -> bool:
        '''
            returns True the first time we run this method after 13:00
            returns False in all other cases
        '''
        # if time now before 13:00
        if timeofday.is_before_time(13, 00):
            self.elspot_tomorrow_check = False
            return False
        # if we have already checked and time is after 13:00
        if self.elspot_tomorrow_check:
            return False
        # time is after 13:00 -> set elspot_tomorrow_check = True and return True
        self.elspot_tomorrow_check = True
        return True

    async def process_tomorrows_elspot(self) -> bool:
        '''
            download and process tomorrows elspot prices
        '''
        api = API()
        is_downloaded = await api.download_elspot()
        if not is_downloaded:
            self.elspot_tomorrow_check = False
            return False
        res = await processelspot.reshape(api.response_body)
        for region in res:
            # ADD METADATA
            region_with_metadata = await processelspot.add_metadata(region)
            payload = await processelspot.plot_date(region_with_metadata)
            res = await sql_elspot.insert_plot_date(payload)
            if not res:
                self.elspot_tomorrow_check = False
                return False
            # INSERT INTO elspot_processed
            res = await sql_elspot.insert_processed_elspot(region_with_metadata)
            if not res:
                raise Exception('InsertError: error inserting processed_elspot into SQL table "elspot_processed"')

        return True
