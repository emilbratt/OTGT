import aiohttp

DAYAHEAD_URL = 'https://www.nordpoolgroup.com/api/marketdata/page/10'


async def download_dayahead(currency: str) -> str:
    http_params = {
        'currency': currency
    }
    clientsession = aiohttp.ClientSession()
    async with clientsession.get(url=DAYAHEAD_URL, params=http_params) as resp:
        status = resp.status
        if status == 200:
            print('LIBELSPOT: downloaded elspot dayahead prices')
            response_text = await resp.text()
        else:
            print(f'LIBELSPOT ERROR: could not download elspot from nordpool, received http code: {status}')
            # set an empty string as result
            response_text = str()

    await clientsession.close()
    return response_text
