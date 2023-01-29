# nordpool exposes different page id's and
# they might change the api in the future
# so we try to match the up-to-date one

# based on the value found in envar NORDPOOL_API_PAGE
# this imports the class Handle() from that specific
# script and returns it

def nordpooldayaheadinit(envar_get: object) -> object:
    '''
    calling this function will return an object reay to use
    '''
    PAGE = envar_get('NORDPOOL_API_PAGE')

    match PAGE:
        case '10':
            from .page10 import Handle
            return Handle(envar_get)

        case 'test':
            from .test import Handle
            return Handle()

        case None:
            print('Error: set an api page via envar NORDPOOL_API_PAGE')
            print('..then re-run script')


        case _:
            print('Error: envar NORDPOOL_API_PAGE is set to:', PAGE)
            print('this is not a valid page')

    # if function did not return any value, we have an error (see above)
    print('---Error---')
    print('path: app/nordpooldayahead')
    print('__name__:', __name__)
    print('__file__:', __file__)
    exit(1)
