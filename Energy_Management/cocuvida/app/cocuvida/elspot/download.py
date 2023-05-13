import asyncio

from cocuvida import libelspot
from cocuvida.environment import env_ini_get
from cocuvida.sqldatabase import elspot as sql_elspot
from cocuvida.timehandle import seconds, timeofday

from .validate import dayahead_today_downloaded, dayahead_tomorrow_downloaded


async def dayahead(elspot_obj: libelspot.Elspot):
    '''
        step 1.
            check if elspot is downloaded and if not, download it
        step 2.
            if downloaded on step 1, process the elspot data
        step 3.
            if 2 completes successfully
                save the downloaded (raw) data to sql-table -> elspot_raw
                save the processed data to sql-table -> elspot_processed
        ..repeat
    '''
    currency = env_ini_get(section='cocuvida', key='elspot_currency')
    while True:
        # todays elspot is served from nordpool until 13:00
        # tomorrows elspot is served from nordpool after 13:00
        if timeofday.is_before_time(13, 0):
            downloaded = await dayahead_today_downloaded()
        else:
            downloaded = await dayahead_tomorrow_downloaded()

        if not downloaded:
            elspot_raw_data = await elspot_obj.download_dayahead(currency)
            if not elspot_obj.download_ok:
                print('ERROR: elspot dayahead raw download failed')
            elif elspot_obj.download_ok:
                elspot_processed_data = await elspot_obj.process_dayahead(elspot_raw_data)
                if not elspot_obj.process_ok:
                    print('ERROR: processing failed for elspot raw data')
                elif elspot_obj.process_ok:
                    sql_result = await sql_elspot.insert_raw_elspot(elspot_raw_data)
                    if not sql_result:
                        print('ERROR: SQL insert failed for elspot dayahead raw data')
                    for elspot_region in elspot_processed_data.values():
                        sql_result = await sql_elspot.insert_processed_elspot(elspot_region)
                        if not sql_result:
                            region = elspot_region['region']
                            print(f'ERROR: SQL insert failed for elspot dayahead processed region {region}')

        await asyncio.sleep(seconds.until_next_hour())
