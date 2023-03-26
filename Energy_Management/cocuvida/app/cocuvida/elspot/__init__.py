import asyncio

from cocuvida.timehandle import timeofday, isodates, seconds

from cocuvida.elspot import nordpooldayahead

async def app():
    from cocuvida.sqldatabase import elspot as sql_elspot
    res = await sql_elspot.elspot_raw_exists_for_date(isodates.today_plus_days(1))
    # while True:
    #     sleep_time = seconds.until_next_minute()
    #     await asyncio.sleep(sleep_time)

    app = nordpooldayahead.Application()
    if await app.elspot_is_published():
        if await app.download():
            pass
            

def run_elspot() -> None:
    asyncio.run(app())
