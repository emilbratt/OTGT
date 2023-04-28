from cocuvida.web.views.elspot import View
from urllib.parse import urlparse, parse_qs, unquote

async def controller(scope: dict, receive: object) -> View:
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
        await view.show_prices(region)
        await view.show_plot(region)
        return view
    return view
