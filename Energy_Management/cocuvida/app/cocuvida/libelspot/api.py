import aiohttp

from cocuvida.environment import env_ini_get
from cocuvida.timehandle import isodates
from cocuvida.sqldatabase import elspot as sql_elspot



class API:
    URL = 'https://www.nordpoolgroup.com/api/marketdata/page/10'

    def __init__(self):
        self.status = None
        self.response_body = None
        self.currency = env_ini_get(section='cocuvida', key='elspot_currency')

    async def download_elspot(self) -> bool:
        session = aiohttp.ClientSession()
        http_params = {
            'currency': self.currency,
        }
        res = False
        async with session.get(url=self.URL, params=http_params) as resp:
            self.status = resp.status
            if resp.status == 200:
                self.response_body = await resp.text()
                res = await sql_elspot.insert_raw_elspot(self.response_body)
                await session.close()
                return res
            else:
                print(f'ERROR: could not download elspot from nordpool, http code: {resp.status}')
                await session.close()
                return False
