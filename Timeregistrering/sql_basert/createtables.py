#!/usr/bin/env python3
import sqlite3
import os
database = os.path.join(
    os.path.dirname(
    os.path.realpath(__file__)
    ),
'data', 'data.db'
)
# CREATE TABLES########################
def createDatabase():
    enableForeign = '''PRAGMA foreign_keys;'''
    createRoleTable = '''
    CREATE TABLE IF NOT EXISTS roles(
    role_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    role_desc   TEXT  NULL,
    role_pay   TEXT  NULL
    );
    '''


    createUserTable = '''
    CREATE TABLE IF NOT EXISTS users(
    user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name   TEXT  NULL,
    role_id    INTEGER NOT NULL,
    FOREIGN KEY (role_id)
       REFERENCES roles (role_id)
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

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(enableForeign)
    cursor.execute(createRoleTable)
    cursor.execute(createUserTable)
    cursor.execute(createWorkTable)
    conn.commit()
    conn.close()
if __name__ == '__main__':
    createDatabase()
