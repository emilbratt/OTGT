import sqlite3

from cocuvida.sqldatabase import DATABASE_FILE

SCRIPT_PATH = './cocuvida/sqldatabase/scripts/'


def run(sql_file: str) -> str:
    res = str()
    with open(SCRIPT_PATH + sql_file, 'r') as f:
        cnxn = sqlite3.connect(DATABASE_FILE)
        try:
            cursor = cnxn.cursor()
            cursor.executescript(f.read())
            cnxn.commit()
            res = True
        except Exception as e:
            print(f'ERROR: {__file__} {type(e)} {e}')
            res = False
        finally:
            cnxn.close()
            return res
