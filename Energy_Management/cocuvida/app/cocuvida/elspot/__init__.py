import asyncio

from . import download, plot


async def app():
    print('ELSPOT START')
    loop = asyncio.get_event_loop()
    download_dayahead = loop.create_task(download.dayahead())
    plot_dayahead = loop.create_task(plot.dayahead_date())
    plot_live = loop.create_task(plot.dayahead_live())
    await download_dayahead
    await plot_dayahead
    await plot_live

def run_elspot() -> None:
    asyncio.run(app())
