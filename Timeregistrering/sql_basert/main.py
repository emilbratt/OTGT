#!/usr/bin/env python3
# Emil Bratt -> emilbratt@gmail.com
import os
from dbclient import connect
# create clear screen function
clearScreen = lambda : os.system(
    'cls' if os.name == 'nt' else 'clear')
database = os.path.join(
    os.path.dirname(
    os.path.realpath(__file__)
    ),
'data', 'data.db'
)

if os.path.isfile(database) == False:
    from createdb import createDatabase
    createDatabase()

def updateRoles():
    c = connect()
    clearScreen()
    c.updateRoles()
    c.commit()
    c.close()

def insertRoles():
    c = connect()
    clearScreen()
    c.insertRoles()
    c.commit()
    c.close()


def deleteRoles():
    c = connect()
    clearScreen()
    c.deleteRoles()
    c.commit()
    c.close()


def printRoles():
    c = connect()
    c.printRoles()
    c.close()


# def insertWork(): # not  finished
#     c = connect()
#     clearScreen()
#     c.insertWork()
#     c.close()

def insertUser():
    c = connect()
    clearScreen()
    c.insertUser()
    c.commit()
    c.close()

if __name__ == '__main__':
    # updateRoles()
    insertRoles()
    # insertUser()
    # printRoles()
    # deleteRoles()
    # insertWork()
