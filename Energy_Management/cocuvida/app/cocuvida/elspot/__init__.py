import asyncio

from cocuvida import libelspot

from . import download, plot


async def app() -> None:
    print('ELSPOT START')
    elspot_obj = libelspot.Elspot()
    asyncio.ensure_future(download.dayahead(elspot_obj))
    asyncio.ensure_future(plot.dayahead_date(elspot_obj))
    asyncio.ensure_future(plot.dayahead_live(elspot_obj))

async def run_elspot() -> None:
    await app()
