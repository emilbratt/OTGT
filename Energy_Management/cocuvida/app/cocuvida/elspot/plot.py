import asyncio

from cocuvida import libelspot
from cocuvida.sqldatabase import elspot as sql_elspot
from cocuvida.timehandle import isodates, seconds, timeofday

from . import validate


async def dayahead_date(elspot_obj: libelspot.Elspot):
    '''
        step 1.
            load processed elspot for yesterday, today and tomorrow from sql-table -> elspot_plot_date
        step 2.
            if data is received, check if plot is generated for each region in received data
        step 3.
            if plit is not generated for that region, generate plot
        step 3.
            if plot was generated, save plot to sql-table -> elspot_plot_date
        ..repeat
    '''
    async def _generate(elspot_obj: libelspot.Elspot, elspot_processed: list) -> None:
        for region_data in elspot_processed:
            region = region_data['region']
            isodate = region_data['date']
            is_generated = await validate.plot_for_date_and_region_generated(region, isodate)
            if not is_generated:
                if await validate.elspot_has_metadata(region_data):
                    plot = await elspot_obj.plot_dayahead_date(region_data)
                    if not elspot_obj.plot_ok:
                        print(f'ERROR: generating dayahead plot failed for {region} {isodate}')
                    else:
                        res = await sql_elspot.insert_plot_date(region, isodate, plot)
                        if not res:
                            print(f'ERROR: saving dayahead plot date to database failed for {region} {isodate}')

    while True:
        today = await sql_elspot.select_processed_for_date(isodates.today())
        yesterday = await sql_elspot.select_processed_for_date(isodates.today_plus_days(-1))
        await _generate(elspot_obj, today)
        await _generate(elspot_obj, yesterday)
        if timeofday.is_passed_time(13, 2): # 13:02 to allow time for elspot download and processing first at 13:00
            tomorrow = await sql_elspot.select_processed_for_date(isodates.today_plus_days(1))
            await _generate(elspot_obj, tomorrow)

        await asyncio.sleep(seconds.until_next_quarter_hour())

async def dayahead_live(elspot_obj: libelspot.Elspot):
    '''
        every 15 minute
            1. on new day or if no data loaded, (re)load todays elspot data
            2. generate a plot with an vertical line marking current time
    '''
    async def _generate(elspot_obj: libelspot.Elspot, elspot_processed: list) -> None:
        for region_data in elspot_processed:
            if await validate.elspot_has_metadata(region_data):
                plot = await elspot_obj.plot_dayahead_live(region_data)
                if not elspot_obj.plot_ok:
                    print(f'ERROR: generating dayahead plot failed for {region} {isodate}')

    date_today = isodates.today()
    elspot_processed = await sql_elspot.select_processed_for_date(date_today)
    while True:
        if elspot_processed == [] or date_today != isodates.today():
            elspot_processed = await sql_elspot.select_processed_for_date(date_today)

        await _generate(elspot_obj, elspot_processed)
        await asyncio.sleep(seconds.until_next_quarter_hour())
