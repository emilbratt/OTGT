from urllib.parse import urlparse, parse_qs, unquote, urlencode

from cocuvida.libelspot import Elspot
from cocuvida.sqldatabase import elspot as sql_elspot
from cocuvida.timehandle import isodates
from cocuvida.web.views.elspot import View


async def controller(scope: dict, receive: object) -> View:
    view = View()
    regions = await sql_elspot.list_elspot_regions()
    rows = []
    for region in regions:
        mapped = {'region': region}
        qs = urlencode(mapped)
        rows.append([f'/elspot?{qs}', region])
    await view.list_elspot_regions(rows)

    region    = None
    time_from = None
    time_to   = None

    qs = scope['query_string']
    qs = unquote(qs)
    qsp = parse_qs(qs, keep_blank_values=False, encoding='utf-8', separator='&')
    for key,val in qsp.items():
        if key == 'region':
            region = val[0]
        elif key == b'time_from':
            time_from = val[0].decode('utf-8')
        elif key == b'time_to':
            time_to = val[0].decode('utf-8')

    if region == None:
        return view
    if time_from == None or time_to == None:
        # show live plot if exist
        plot_svg = await Elspot().get_plot_dayahead_live(region)
        if plot_svg != '':
            await view.show_plot(plot_svg)
        # show tomorrows plot if exist
        plot_svg = await sql_elspot.select_plot_for_date_and_region(isodates.today_plus_days(1), region)
        if plot_svg != '':
            await view.show_plot(plot_svg)
        return view
    return view
