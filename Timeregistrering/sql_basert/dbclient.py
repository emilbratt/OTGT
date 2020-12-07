#!/usr/bin/env python3
import sqlite3
import os
from visual import userConfirm, listMatrix, tupleMatrix, clearScreen, getUserValues,getUserValue, message, messages, emptyQuery
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
);
'''
work = [
('1','2020-12-04','08:00','16:00','5','49','8.00'),
('2','2020-12-04','09:10','16:00','5','49','6.50'),
('1','2018-12-04','09:10','16:00','5','49','6.50'),
]
####################################################

# insert roles #####################################
insertRoles = '''
INSERT INTO roles(
role_desc,
role_category
)
VALUES (
    ?,?
);
'''
####################################################

# print roles ######################################
printRoles = '''SELECT * FROM roles;'''

printRoleID = '''
SELECT roles.role_desc, roles.role_category
FROM
    roles
WHERE
    role_id=?;
'''
####################################################

# delete roles #####################################
deleteRoles = '''
DELETE FROM roles
WHERE
    role_id=?;
'''
####################################################

# update roles #####################################
updateRoles = '''
UPDATE roles
SET
    role_desc=?,
    role_category=?
WHERE
    role_id=?;
'''
#####################################################

# insert user #######################################
insertUser = '''
INSERT INTO users (
    user_name,
    role_id
)
VALUES (
    ?,?
)
'''
#####################################################

# print users ######################################
printUsers = '''
SELECT
    user_name
FROM
    users;
'''
printAllUsers = '''
SELECT
    *
FROM
    users;
'''


def printRoleTable(cursor):
    head = ['Rolle ID','Rolle Navn','Rolle Kategori']
    cursor.execute(printRoles)
    queryRes = cursor.fetchall()
    if emptyQuery(queryRes, 'Rollelisten er tom') == True:
        return None
    message('Rolletabell')
    tupleMatrix(head,queryRes,3,False)



def printUserTable(cursor):
    head = ['Brukernavn']
    cursor.execute(printUsers)
    queryRes = cursor.fetchall()
    if emptyQuery(queryRes, 'Ingen brukere er lagt til') == True:
        return None
    message('Brukere')
    tupleMatrix(head,queryRes,1,False)


def printAllUsersTable(cursor):
    head = ['Bruker ID','Brukernavn','Rolle Id']
    cursor.execute(printAllUsers)
    queryRes = cursor.fetchall()
    if emptyQuery(queryRes, 'Ingen brukere er lagt til') == True:
        return None
    message('Brukere')
    tupleMatrix(head,queryRes,3,False)


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
        if userConfirm('Vil du se rolle tabellen først?',True) == True:
            printRoleTable(self.cursor)
        message('Legg verdier i rolletabellen')
        title = ['Legg til rolle','Legg til Kategori']
        head = ['Rolle','Kategori']
        values = getUserValues(2,title)
        if values == None:
            return None
        tupleMatrix(head,values,2)
        if userConfirm('Disse verdiene blir lagt til, OK?') == True:
            self.cursor.executemany(insertRoles,values)
        else:
            return None


    def printRoles(self):
        head = ['Rolle ID','Rolle Navn','Rolle Kategori']
        self.cursor.execute(printRoles)
        queryRes = self.cursor.fetchall()
        message('Rolletabell')
        tupleMatrix(head,queryRes,3,False)


    def updateRoles(self):

        head = ['Rolle Navn','Kategori']
        headUpdate = ['Nytt Rolle Navn','Ny Kategori']
        title = ['Velg Rolle ID']
        clearScreen()
        if userConfirm('Vil du se rolle tabellen først?',True) == True:
            printRoleTable(self.cursor)
        message('Velg id på oppføringen du vil endre')
        id = getUserValue(1,title)
        if id == None:
            return None
        queryRes = []
        # list record that will be updated
        for i in range(len(id)):
            self.cursor.execute(printRoleID,id[i])
            queryRes.append(self.cursor.fetchone())

        # if no records(no id where selected from user), end function
        if queryRes == [None]:
            return None
        message('Endrer på denne oppføringen')
        tupleMatrix(head,queryRes,2)

        values = getUserValue(2,headUpdate)
        if values == None:
            return None
        clearScreen()
        message('Før')
        tupleMatrix(head,queryRes,2,False)
        message('etter')
        tupleMatrix(head,values,2,False)
        parameters = [values[0][0],values[0][1],id[0][0]]

        if userConfirm('Vil du lagre endringen?',False) == True:
            self.cursor.execute(updateRoles,parameters)
        else:
            return None


    def deleteRoles(self):
        head = ['Rolle Navn','Kategori']
        title = ['Velg Rolle ID']
        clearScreen()
        if userConfirm('Vil du se oversikt over roller først?',True) == True:
            printRoleTable(self.cursor)

        # fetch id from user
        message('Fjern oppføring i rolletabellen')
        values = getUserValues(1,title)
        if values == None:
            return None
        queryRes = []

        # list records that will be removed
        for i in range(len(values)):
            self.cursor.execute(printRoleID,values[i])
            queryRes.append(self.cursor.fetchone())

        # if no records(no id where selected from user), end function
        if queryRes == [None]:
            return None
        tupleMatrix(head,queryRes,2)

        message('Endre oppføring i rolletabellen')
        values = getUserValues(2,head)
        return None
        if userConfirm('Roller vist over blir fjernet, ok?') == True:
            self.cursor.executemany(deleteRoles,values)
        else:
            return None

# 'user_id','workdate','from_clock',
# 'to_clock','week_day','week_number','total_time'
    def insertUser(self):
        clearScreen()
        if userConfirm('Vil du se oversikt over brukere først?',True) == True:
            printAllUsersTable(self.cursor)

        head = ['Brukernavn']
        head2 = ['Rolle','Kategori']
        head3 = ['Brukernavn','Rolle','Kategori']
        title = ['Legg til brukernavn']
        title2 = ['Velg rolle']
        userName = getUserValue(1,title,False)
        if userName == None:
            return None

        tupleMatrix(head,userName,1)
        queryRes = []
        parameters = []
        if userConfirm('Vil du velge rolle for brukeren?',True) == True:
            if userConfirm('Vil du se rolle tabellen først?',True) == True:
                printRoleTable(self.cursor)
            # message('Velg rolle')
            roleID = getUserValue(1,title2,False)
            if roleID == None:
                return None

            for i in range(len(roleID)):
                self.cursor.execute(printRoleID,roleID[i])
                queryRes.append(self.cursor.fetchone())
            if queryRes == [None]:
                return None

            row = []

            row.append(userName[0][0])
            row.append(queryRes[0][0])
            row.append(queryRes[0][1])
            parameters.append(userName[0][0])
            parameters.append(roleID[0][0])
            # summary = [tuple(values)]

            # tupleMatrix(head3,summary,3,True)
            listMatrix(head3,row,3,True)
            if userConfirm('Disse verdiene blir lagt til, OK?') == True:
                self.cursor.execute(insertUser,parameters)
        else:
            tupleMatrix(head,userName,1,False)
            if userConfirm('Denne brukeren blir lagt til, OK?') == True:
                self.cursor.execute(insertUser,[userName[0][0],('0')])
