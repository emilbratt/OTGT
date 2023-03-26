import asyncio
import json

from cocuvida.elspot.nordpooldayahead import process

FILES = {
    '23': 'tests/test_data/elspot/23/2023-03-26.json',
    '24': 'tests/test_data/elspot/24/2022-12-01.json',
    '25': 'tests/test_data/elspot/25/2022-10-30.json',
}


def daylight_saving_case(self):
    '''
        The entire year except for 2 days, we have 24 hours during the day
        For the remaining 2, we have either 23 or 25 depending on wether we are
        moving from summer to winter-time or from winter to summer-time.

        This test uses elspot data fetched from nordpool.
        One version for each of the 3 cases (23, 24 and 25 hours).
    '''
    with open(FILES['23']) as f:
        data = asyncio.run(process.reshape(f.read()))
        self.assertTrue(data[0]['resolution'] == 92)

    with open(FILES['24']) as f:
        data = asyncio.run(process.reshape(f.read()))
        self.assertTrue(data[0]['resolution'] == 96)

    with open(FILES['25']) as f:
        data = asyncio.run(process.reshape(f.read()))
        self.assertTrue(data[0]['resolution'] == 100)