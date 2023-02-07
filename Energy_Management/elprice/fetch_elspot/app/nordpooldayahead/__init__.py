# nordpool exposes different page id's and
# they might change the api in the future
# so we try to match the up-to-date one

# based on the value found in envar NORDPOOLDAYAHEAD_API_VERSION
# this imports the class Handle() from that specific
# script and returns it

URL_LIST = {
    'test': 'http://192.168.0.207:8082/download/hourly/2023-01-23.json',
    'page_10': 'https://www.nordpoolgroup.com/api/marketdata/page/10',
}

def nordpooldayaheadinit(envar_get: object, isodate: object) -> object:
    '''
    calling this function will return an object reay to use
    '''
    api_version = envar_get('NORDPOOLDAYAHEAD_API_VERSION')
    match api_version:
        case '0':
            from .api0 import Handle
            handle = Handle(envar_get)
        case '1':
            from .api1 import Handle
            handle = Handle(envar_get=envar_get, isodate=isodate, url=URL_LIST['page_10'])
        case None:
            print('Error:')
            print('envar NORDPOOLDAYAHEAD_API_VERSION not set')
            exit(1)
        case _:
            print('Error:')
            print('envar NORDPOOLDAYAHEAD_API_VERSION is invalid, currenclty set to:', api_version)
            exit(1)

    return handle
