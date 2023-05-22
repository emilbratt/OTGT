import sqlite3

DATABASE_FILE = 'data.sqlite'

# use connet() when granularity is of concern
# use the other functions when simplicity is wanted

def connect() -> sqlite3.connect:
    cnxn = sqlite3.connect(DATABASE_FILE)
    return cnxn

def insert_one(query: str, row: list) -> str:
    cnxn = sqlite3.connect(DATABASE_FILE)
    cursor = cnxn.cursor()
    try:
        cursor.execute(query, row)
        cnxn.commit()
        res = 'insert'
    except sqlite3.IntegrityError:
        res = 'IntegrityError'
    except Exception as e:
        res = f'ERROR: {__file__} {type(e)} {e}'
    finally:
        cnxn.close()
        return res

def insert_many(query: str, rows: list) -> None:
    cnxn = sqlite3.connect(DATABASE_FILE)
    cursor = cnxn.cursor()
    cursor.executemany(query, rows)
    cnxn.commit()
    cnxn.close()

def update(query: str, row: list) -> str:
    cnxn = sqlite3.connect(DATABASE_FILE)
    cursor = cnxn.cursor()
    try:
        cursor.execute(query, row)
        cnxn.commit()
        res = 'update'
    except Exception as e:
        res = f'ERROR: {__file__} {type(e)} {e}'
    finally:
        cnxn.close()
        return res

def select_one(query: str, param: list) -> list:
    cnxn = sqlite3.connect(DATABASE_FILE)
    cursor = cnxn.cursor()
    cursor.execute(query, param)
    res = cursor.fetchone()
    cnxn.close()
    return res

def select_one_no_param(query: str) -> list:
    cnxn = sqlite3.connect(DATABASE_FILE)
    cursor = cnxn.cursor()
    cursor.execute(query)
    res = cursor.fetchone()
    cnxn.close()
    return res

def select_all(query: str, param: list) -> list:
    cnxn = sqlite3.connect(DATABASE_FILE)
    cursor = cnxn.cursor()
    cursor.execute(query, param)
    res = cursor.fetchall()
    cnxn.close()
    return res

def select_all_no_param(query: str) -> list:
    cnxn = sqlite3.connect(DATABASE_FILE)
    cursor = cnxn.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    cnxn.close()
    return res

def delete(query: str, param: list) -> list:
    cnxn = connect()
    cursor = cnxn.cursor()
    try:
        cursor.execute(query, param)
        cnxn.commit()
        action = 'delete'
    except Exception as e:
        action = f'ERROR: {__file__} {type(e)} {e}'
    finally:
        cnxn.close()
        return action
