import asyncio
import json

from cocuvida.nordpooldayahead import processelspot
from cocuvida.sqldatabase import elspot as sql_elspot

FILES = {
    23: 'tests/test_data/elspot/23/2023-03-26.json',
    24: 'tests/test_data/elspot/24/2022-12-01.json',
    25: 'tests/test_data/elspot/25/2022-10-30.json',
}


def process_elspot(self, hour: int, expected_resolution: int):
    '''
        The entire year except for 2 days consists of 24 hours.
        For the remaining 2 we have either 23 or 25 depending on wether we are
        moving from summer to winter-time or from winter to summer-time.

        This test uses elspot data fetched from nordpool.
        One version for each of the 3 cases (23, 24 and 25 hours).

        The resolution (total N quarters) for the 3 different cases are as follows:
            23 = 92  ( 23 x 4 )
            24 = 96  ( 24 x 4 )
            25 = 100 ( 25 x 4 )
            .. we test this by passing the excpeted resolution as a parameter
    '''
    with open(FILES[hour]) as f:
        raw_elspot = f.read()
        processed_elspot = asyncio.run(processelspot.reshape(raw_elspot))
        # check if resoultion checks out
        self.assertTrue(processed_elspot[0]['resolution'] == expected_resolution)
        # insert raw into database
        asyncio.run(sql_elspot.insert_raw_elspot(raw_elspot))
        check_set = {'Oslo': False, 'Tr.heim': False, 'DK1': False, 'SE1': False}
        for region in processed_elspot:
            match region['region']:
                case 'Oslo'|'Tr.heim'|'DK1'|'SE1':
                    check_set[region['region']] = True
                    # insert reshaped versions for each region into database
                    res = asyncio.run(sql_elspot.insert_processed_elspot(region))
                    self.assertTrue(res)
                    # generate plot from the reshaped version
                    payload = asyncio.run(processelspot.plot_date(region))
                    res = asyncio.run(sql_elspot.insert_plot_date(payload))
                    self.assertTrue(res)
        # this checks if the match block ran the 4 expected entries
        for region in check_set:
            self.assertTrue(check_set[region])
