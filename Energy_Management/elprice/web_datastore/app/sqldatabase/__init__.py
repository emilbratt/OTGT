from os import path

def sqldatabasecrud(envar_get: object) -> object:
    '''
        crud operations
    '''
    from .crud import Tables
    databasefile = path.join(envar_get('DIR_DATABASE'), 'data.sqlite')
    return Tables(databasefile)

def sqldatabasemanage(envar_get: object) -> object:
    '''
        create/delete database, tables, etc
    '''
    from .manage import Tables
    databasefile = path.join(envar_get('DIR_DATABASE'), 'data.sqlite')
    return Tables(databasefile)
