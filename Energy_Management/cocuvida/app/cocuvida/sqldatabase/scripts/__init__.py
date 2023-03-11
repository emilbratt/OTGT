import sqlite3
from os import path

from cocuvida.sqldatabase import DATABASE_FILE

def run(script: str):
    sciript_dir = path.dirname(path.realpath(__file__))
    transaction_ok = None
    with open(path.join(sciript_dir, script), 'r') as f:
        cnxn = sqlite3.connect(DATABASE_FILE)
        try:
            cursor = cnxn.cursor()
            cursor.executescript(f.read())
            transaction_ok = True
        except:
            transaction_ok = False
        finally:
            cnxn.close()
            return transaction_ok
