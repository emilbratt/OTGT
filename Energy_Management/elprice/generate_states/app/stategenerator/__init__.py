def stateinit(envar_get: object) -> object:
    API_VERSION = envar_get('STATE_GENERATOR_API_VERSION')

    match API_VERSION:
        case '0':
            from .api0 import Handle
            return Handle

        case None:
            print('Error: missing envar')
            print('..set an api page via envar HTTPDATASTORE_API_VERSION')

        case _:
            print('Error: invalid envar:', API_VERSION)

    print('namespace:', __name__+ '.Handle()')
    print('script:', __file__)
    exit(1)
