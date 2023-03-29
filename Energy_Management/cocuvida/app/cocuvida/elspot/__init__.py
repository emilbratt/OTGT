import asyncio

from cocuvida.timehandle import seconds, timeofday
from cocuvida import nordpooldayahead


async def app():
    print('ELSPOT START')
    app = nordpooldayahead.Application()
    await app.on_startup()
    while True:
        if await app.elspot_is_published():
            await app.process_tomorrows_elspot()
        await app.on_every_quarter()
        sleep_time = seconds.until_next_quarter_hour()
        print('ELSPOT: sleep seconds', sleep_time, 'time now', timeofday.now())
        await asyncio.sleep(sleep_time)

def run_elspot() -> None:
    asyncio.run(app())
