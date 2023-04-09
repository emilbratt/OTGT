import asyncio

from cocuvida.timehandle import seconds, timeofday
from cocuvida import libelspot


async def app():
    print('ELSPOT START')
    elspot = libelspot.Elspot()
    await elspot.on_startup()
    while True:
        if await elspot.elspot_is_published():
            await elspot.process_tomorrows_elspot()
        await elspot.generate_live_plots()
        sleep_time = seconds.until_next_quarter_hour()
        await asyncio.sleep(sleep_time)

def run_elspot() -> None:
    asyncio.run(app())
