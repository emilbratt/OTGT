from os import path

def sqldatabaseschema(envar_get: object) -> object:
    '''
        manage database tables
    '''
    from .schema import Tables
    return Tables(envar_get('DATABASE_FILE'))

def sqldatabasecrud(envar_get: object) -> object:
    '''
        database crud operations
    '''
    from .crud import Tables
    return Tables(envar_get('DATABASE_FILE'))
