import aiohttp

from cocuvida.environment import env_ini_get
from cocuvida.timehandle import isodates
from cocuvida.sqldatabase import elspot as sql_elspot

URL = 'https://www.nordpoolgroup.com/api/marketdata/page/10'


class API:
    def __init__(self):
        self.status = None
        self.response_body = None

    async def download(self) -> bool:
        session = aiohttp.ClientSession()
        params = {
            'currency': env_ini_get(section='cocuvida', key='elspot_currency'),
            'endDate': isodates.today_plus_days(1),
        }
        res = False
        async with session.get(URL, params=params) as resp:
            self.status = resp.status
            if resp.status == 200:
                self.response_body = await resp.text()
                res = await sql_elspot.insert_raw_elspot(self.response_body)
            await session.close()
            return res
