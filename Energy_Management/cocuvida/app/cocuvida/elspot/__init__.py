import asyncio

from cocuvida import libelspot

from . import download, plot


async def app() -> None:
    print('ELSPOT START')
    elspot_obj = libelspot.Elspot()
    loop = asyncio.get_running_loop()
    loop.create_task(download.dayahead(elspot_obj))
    loop.create_task(plot.dayahead_date(elspot_obj))
    loop.create_task(plot.dayahead_live(elspot_obj))

async def run_elspot() -> None:
    await app()
