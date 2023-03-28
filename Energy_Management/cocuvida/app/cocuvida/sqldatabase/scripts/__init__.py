import sqlite3
from os import path

from cocuvida.sqldatabase import DATABASE_FILE


def run(script: str) -> str:
    sciript_dir = path.dirname(path.realpath(__file__))
    res = str()
    with open(path.join(sciript_dir, script), 'r') as f:
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
