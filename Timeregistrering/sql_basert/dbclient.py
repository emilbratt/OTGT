#!/usr/bin/env python3
import sqlite3
import os
from visual import continueAsk, listMatrix, tupleMatrix, clearScreen
database = os.path.join(
    os.path.dirname(
    os.path.realpath(__file__)
    ),
'data', 'data.db'
)
insertWork = '''
INSERT INTO work(
'user_id','workdate','from_clock',
'to_clock','week_day','week_number','total_time'
) VALUES (
?,?,?,?,?,?,?
)'''
work = [
('1','2020-12-04','08:00','16:00','5','49','8.00'),
('2','2020-12-04','09:10','16:00','5','49','6.50'),
('1','2018-12-04','09:10','16:00','5','49','6.50'),
]

insertRoles = '''
INSERT INTO roles(
role_desc, role_pay
) VALUES (
?,?
)
'''
printRoles = '''SELECT * FROM roles;'''

def mergeList(string):
    L = list(string.split(" "))
    return L

def getUserValues(N,M=''):
 # N = numbers of columns to insert
 # M = Message
    LT = []
    while True:
        L = []
        print(M)
        for i in range(N):
            k = input('skriv: ')
            L.append(k)
            if i == (N-1):
                L = tuple(L)
                LT.append(L)
                L = []
                if continueAsk() == False:
                    return LT



class connect:
    def __init__(self):
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def insertRoles(self):
        clearScreen()
        values = getUserValues(2,'Legg til verdier')
        tupleMatrix(values,2)
        if continueAsk() == False:
            return None
        else:
            self.cursor.executemany(insertRoles,values)

    def printRoles(self):
        self.cursor.execute(printRoles)
        print('roles')
        input(self.cursor.fetchall())
