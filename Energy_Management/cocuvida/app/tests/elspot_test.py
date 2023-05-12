import asyncio
import json
import unittest

from cocuvida import libelspot
from cocuvida.sqldatabase import elspot as sql_elspot

FILES = {
    # this is the most "normal" case of elspot prices (nothing out of the ordinary here..)
    'normal': 'tests/test_data/elspot/normal/2022-12-01.json',

    # these files contains elsopt prices for non-24 hour days (for dailight savings time cases)
    '23': 'tests/test_data/elspot/23/2023-03-26.json',
    '25': 'tests/test_data/elspot/25/2022-10-30.json',

    # this file contains elspot prices that are below zero
    'negative': 'tests/test_data/elspot/negative/2023-04-10.json',
}


def process_elspot(self: unittest.TestCase, file_ref: str, expected_resolution: int):
    '''
        The entire year except for 2 days consists of 24 hours.
        For the remaining 2 we have either 23 or 25 depending on wether we are
        moving from summer to winter-time or from winter to summer-time.

        This test uses elspot data fetched from https://www.nordpoolgroup.com/api/marketdata/page/10.
        One version for each of the 3 cases (23, 24 and 25 hours).

        By future-proofing we also split each hour up into 4 quarters.
        We are moving from hourly to quarterly resolution e.g. 15 minutes metering.
        See https://www.statnett.no/en/for-stakeholders-in-the-power-industry/system-operation/the-power-market/quarterly-resolution-and-the-energy-markets/
        The resolution (total N quarters) for the 3 different cases are as follows:
            23h = 92 indexes  -> 23 x 4
            24h = 96 indexes  -> 24 x 4
            25h = 100 indexes -> 25 x 4
            .. we also test the resolution by passing the number "expected_resolution" as a parameter
    '''
    with open(FILES[file_ref]) as f:
        raw_elspot = f.read()

        # INSERT RAW ELSPOT DATA INTO DATABASE
        asyncio.run(sql_elspot.insert_raw_elspot(raw_elspot))

        # PROCESS ELSPOT
        elspot_obj = libelspot.Elspot()
        processed_elspot = asyncio.run(elspot_obj.process_dayahead(raw_elspot))
        self.assertTrue(processed_elspot['Molde']['resolution'] == expected_resolution)

        # INSERT PROCESSED ELSPOT INTO DATABASE
        for elspot_data in processed_elspot.values():
            # insert reshaped versions for each region into database
            res = asyncio.run(sql_elspot.insert_processed_elspot(elspot_data))
            self.assertTrue(res)

        # GENERATE PLOTS (WE ONLY GENERATE FOR 4 SELECT REGIONS AS THIS IS TIME CONSUMING)
        generate_plot_for = {'Oslo': False, 'Tr.heim': False, 'DK1': False, 'SE1': False}
        for elspot_region, elspot_data in processed_elspot.items():
            match elspot_region:
                # plot generator takes some time, only do processing for select regions
                case 'Oslo'|'Tr.heim'|'DK1'|'SE1':
                    generate_plot_for[elspot_region] = True

                    # GENERATE NORMAL DATE PLOT
                    plot = asyncio.run(elspot_obj.plot_dayahead_date(elspot_data))
                    res = asyncio.run(sql_elspot.insert_plot_date(elspot_data['region'], elspot_data['date'], plot))
                    self.assertTrue(res)

                    # GENERATE LIVE PLOT (THIS INCLUDES THE TIME OF DAY MARKER)
                    if elspot_data['date'] == '2023-03-26':
                        # only one live plot can be stored at once, so we only generate for one date
                        plot = asyncio.run(elspot_obj.plot_dayahead_live(elspot_data))
                        res = asyncio.run(sql_elspot.insert_plot_live(elspot_data['region'], plot))
                        self.assertTrue(res)

        # this checks if select regions actually where processed
        for region in generate_plot_for:
            self.assertTrue(generate_plot_for[region])
