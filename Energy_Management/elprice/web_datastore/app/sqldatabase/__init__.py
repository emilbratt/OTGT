from os import path

def sqldatabasecrud(envar_get: object) -> object:
    '''
        crud operations
    '''
    from .crud import Tables
    databasefile = envar_get('DATABASE_FILE')
    return Tables(databasefile)

def sqldatabasemanage(envar_get: object) -> object:
    '''
        create/delete database, tables, etc
    '''
    from .manage import Tables
    databasefile = envar_get('DATABASE_FILE')
    return Tables(databasefile)
