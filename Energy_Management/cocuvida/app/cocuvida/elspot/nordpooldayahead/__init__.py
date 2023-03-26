import aiohttp

from cocuvida.timehandle import timeofday, isodates

from . import process
from .api import API


class Application:
    URL = 'https://www.nordpoolgroup.com/api/marketdata/page/10'

    def __init__(self):
        self.url = self.URL
        self.status = None
        self.raw_data = None
        self.reshaped_data = None
        self.elspot_is_published_check = False

    async def elspot_is_published(self) -> bool:
        '''
            returns True one time the first time we run this method after 13:30
            returns False in all other cases
        '''
        # if time now before 13:30
        if timeofday.is_before_time(13, 30):
            self.elspot_is_published_check = False
            return False
        # if we have already checked and time is after 13:30
        if self.elspot_is_published_check:
            return False
        # time is after 13:30 -> set elspot_is_published_check = True and return True
        self.elspot_is_published_check = True
        return True

    async def download(self) -> bool:
        api = API()
        if await api.download():
            self.reshaped_data = await process.reshape(api.response_body)
            return True
        return False
