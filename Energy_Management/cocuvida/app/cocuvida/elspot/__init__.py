from cocuvida.timehandle import isodates, seconds, timeofday

from .currency import get as get_region_config


class Elspot:

    URL = 'https://www.nordpoolgroup.com/api/marketdata/page/10'

    def __init__(self):
        self.region_config = get_region_config()
        print(self.region_config)
        print(isodate.today())


def run_elspot():
    app = Elspot()
