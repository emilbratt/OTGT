import asyncio

from . import download, plot


async def app():
    print('ELSPOT START')
    asyncio.ensure_future(download.dayahead())
    asyncio.ensure_future(plot.dayahead_date())
    asyncio.ensure_future(plot.dayahead_live())

async def run_elspot() -> None:
    await app()
