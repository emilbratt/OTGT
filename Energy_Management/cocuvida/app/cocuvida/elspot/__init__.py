import asyncio

from cocuvida.timehandle import timeofday, isodates, seconds

from .currency import get as get_region_config


class Elspot:

    URL = 'https://www.nordpoolgroup.com/api/marketdata/page/10'

    def __init__(self):
        self.region_config = get_region_config()
        print(self.region_config)
        print(isodates.today())

async def app():
    el = Elspot()

def run_elspot() -> None:
    asyncio.run(app())
