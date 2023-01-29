def sqldatabaseinit(envar_get: object) -> object:
    '''
        create database if not exists, or just validate it
        then return Entities
    '''
    from os import path
    databasefile = path.join(envar_get('DIR_DATABASE'), 'data.sqlite')

    # for first ever run, the database must be created, and tables too..
    if not path.exists(databasefile):
        import sqlite3
        from .tablegenerate import TABLE_MAP
        cnxn = sqlite3.connect(databasefile)
        cursor = cnxn.cursor()
        for table in TABLE_MAP:
            create_table = TABLE_MAP[table]['create']
            cursor.execute(create_table)
            cnxn.commit()
        cnxn.close()

    from .entities import Entities
    return Entities(databasefile)
