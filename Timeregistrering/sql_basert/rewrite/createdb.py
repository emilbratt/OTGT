#!/usr/bin/env python3
import sqlite3
import os
from password import passwordStore
from visual import getUserValue
dataPath = database = os.path.join(
    os.path.dirname(
    os.path.realpath(__file__)
    ),
    'data'
)

database = os.path.join(
    os.path.dirname(
    os.path.realpath(__file__)
    ),
    'data', 'data.db'
)

# if no datadir, create new
os.makedirs(dataPath, exist_ok=True)

# CREATE TABLES ########################
def createDatabase():
    enableForeignKey = '''PRAGMA foreign_keys;'''

    createUserTable = '''
    CREATE TABLE IF NOT EXISTS users(
        user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name   TEXT NOT NULL,
        password    TEXT NOT NULL
        );
    '''

    createWorkTable = '''
    CREATE TABLE IF NOT EXISTS work(
        user_id     INTEGER NOT NULL,
        workdate   TEXT NOT NULL,
        from_clock  TEXT NOT NULL,
        to_clock    TEXT NOT NULL,
        week_day     TINYINT NOT NULL,
        week_number  TINYINT NOT NULL,
        total_time  TEXT NOT NULL,
        FOREIGN KEY (user_id)
           REFERENCES users (user_id)
        );
    '''

    addRootUser = '''
    INSERT INTO users (
        user_name,
        password
    )
    VALUES (
        'root',?
    );
    '''

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(enableForeignKey)
    cursor.execute(createUserTable)
    cursor.execute(createWorkTable)
    value = getUserValue(1,['skriv inn passord for rot-bruker'])
    rootPWD = passwordStore(value)

    cursor.execute(addRootUser,rootPWD)
    conn.commit()
    conn.close()
if __name__ == '__main__':
    createDatabase()
