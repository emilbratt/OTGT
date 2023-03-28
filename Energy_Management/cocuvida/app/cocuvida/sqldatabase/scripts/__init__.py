import sqlite3
from os import path

from cocuvida.sqldatabase import DATABASE_FILE


def run(script: str) -> str:
    sciript_dir = path.dirname(path.realpath(__file__))
    action = str()
    with open(path.join(sciript_dir, script), 'r') as f:
        cnxn = sqlite3.connect(DATABASE_FILE)
        try:
            cursor = cnxn.cursor()
            cursor.executescript(f.read())
            cnxn.commit()
            action = 'OK'
        except Exception as e:
            action = f'ERROR: {__file__} {type(e)} {e}'
        finally:
            cnxn.close()
            return action
