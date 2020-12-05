#!/usr/bin/env python3
import sqlite3
import os
from visual import userConfirm, listMatrix, tupleMatrix, clearScreen, getUserValues, message, messages, emptyQuery
database = os.path.join(
    os.path.dirname(
    os.path.realpath(__file__)
    ),
'data', 'data.db'
)

# insert work #####################################
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
####################################################

# insert roles #####################################
insertRoles = '''
INSERT INTO roles(
role_desc, role_category
) VALUES (
?,?
)
'''

####################################################

# print roles ##################################
printRoles = '''SELECT * FROM roles;'''

printRoleID = '''
SELECT roles.role_desc, roles.role_category
FROM roles
WHERE role_id=?;
'''
####################################################

# delete roles #####################################
deleteRoles = '''
DELETE FROM roles
WHERE role_id=?;
'''
####################################################


def mergeList(string):
    L = list(string.split(" "))
    return L





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
        message('Legg verdier i rolletabellen')
        clearScreen()
        L = ['Legg til rolle','Legg til Kategori']
        H = ['Rolle','Kategori']
        values = getUserValues(2,L)
        tupleMatrix(H,values,2)
        if userConfirm('Vil du legge til disse verdiene?') == True:
            self.cursor.executemany(insertRoles,values)
        else:
            return None


    def printRoles(self):
        H = ['Rolle ID','Rolle Navn','Rolle Kategori']
        self.cursor.execute(printRoles)
        queryRes = self.cursor.fetchall()
        message('Rolletabell')
        tupleMatrix(H,queryRes,3,False)


    def deleteRoles(self):
        H = ['Rolle Navn','Kategori']
        L = ['Velg Rolle ID']
        clearScreen()
        if userConfirm('Vil du se rolle tabellen først?',True) == True:
            Ht = ['Rolle ID','Rolle Navn','Rolle Kategori']
            self.cursor.execute(printRoles)
            queryRes = self.cursor.fetchall()
            if emptyQuery(queryRes, 'Rollelisten er tom') == True:
                return None
            message('Rolletabell')
            tupleMatrix(Ht,queryRes,3,False)

        # fetch id from user
        message('Fjern oppføring i rolletabellen')
        values = getUserValues(1,L)
        queryRes = []

        # list records that will be removed
        for i in range(len(values)):
            self.cursor.execute(printRoleID,values[i])
            queryRes.append(self.cursor.fetchone())

        # if no records(no id where selected from user), end function
        if queryRes == [None]:
            return None

        tupleMatrix(H,queryRes,2)

        if userConfirm('Roller vist over blir fjernet, ok?') == True:
            self.cursor.executemany(deleteRoles,values)
        else:
            return None
