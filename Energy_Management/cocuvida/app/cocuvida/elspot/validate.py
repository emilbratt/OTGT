from cocuvida.sqldatabase import elspot as sql_elspot
from cocuvida.timehandle import isodates


async def dayahead_today_downloaded() -> bool:
    res = await sql_elspot.elspot_raw_exists_for_date(isodates.today())
    return res

async def dayahead_tomorrow_downloaded() -> bool:
    res = await sql_elspot.elspot_raw_exists_for_date(isodates.today_plus_days(1))
    return res

async def plot_for_date_and_region_generated(region: str, isodate: str) -> bool:
    res = await sql_elspot.plot_for_date_and_region_exist(region, isodate)
    return res

async def elspot_has_metadata(region_data: dict) -> bool:
    return region_data['metadata']
