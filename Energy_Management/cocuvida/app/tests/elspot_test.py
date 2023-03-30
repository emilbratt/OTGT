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
        # insert raw into database
        asyncio.run(sql_elspot.insert_raw_elspot(raw_elspot))

        # RESHAPE ELSPOT
        reshaped_elspot = asyncio.run(processelspot.reshape(raw_elspot))
        # check if resoultion checks out
        self.assertTrue(reshaped_elspot[0]['resolution'] == expected_resolution)

        # INSERT PROCESSED ELSPOT INTO DATABASE
        for region in reshaped_elspot:
            # insert reshaped versions for each region into database
            res = asyncio.run(sql_elspot.insert_processed_elspot(region))
            self.assertTrue(res)

        # ADD METADATA TO PROCESSED ELSPOT (IN A NEW LIST AS WELL)
        metadata_added_elspot = []
        for region in reshaped_elspot:
            name = region['region']
            res = asyncio.run(processelspot.add_metadata(region))
            metadata_added_elspot.append(res)

        # INSERT PROCESSED ELSPOT (WITH ADDED METADATA) INTO DATABASE
        for region in metadata_added_elspot:
            # this will update the previous processed elspot prices
            res = asyncio.run(sql_elspot.insert_processed_elspot(region))
            self.assertTrue(res)

        # GENERATE PLOTS
        check_set = {'Oslo': False, 'Tr.heim': False, 'DK1': False, 'SE1': False}
        for region in reshaped_elspot:
            match region['region']:
                # plot generator takes some time, only do processing for select regions
                case 'Oslo'|'Tr.heim'|'DK1'|'SE1':
                    check_set[region['region']] = True
                    payload = asyncio.run(processelspot.plot_date(region))
                    res = asyncio.run(sql_elspot.insert_plot_date(payload))
                    self.assertTrue(res)
        # this checks if select regions actually where processed
        for region in check_set:
            self.assertTrue(check_set[region])
