from cocuvida.web.views.elspot.prices import View
from urllib.parse import urlparse, parse_qs, unquote

async def controller(scope: dict, receive: object):
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

    view = View()
    await view.list_elspot_regions()
    if region == None:
        return view
    if time_from == None or time_to == None:
        await view.show_prices_for_today(region)
        await view.show_plot_for_today(region)
        return view
    return view
    
    # if time_from == None or time_to == None:
    #     await view.show_prices_for_region_and_time_window(time_from, time_to)
    #a = parse_qs(scope['query_string'], keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace', max_num_fields=None, separator='&')
