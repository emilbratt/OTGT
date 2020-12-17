#!/usr/bin/env python3
# Emil Bratt -> emilbratt@gmail.com
import os
from dbclient import connect # not created yet
# create clear screen function
clearScreen = lambda : os.system(
    'cls' if os.name == 'nt' else 'clear')
database = os.path.join(
    os.path.dirname(
    os.path.realpath(__file__)
    ),
'data', 'data.db'
)



def insertUser():
    c = connect()
    clearScreen()
    c.insertUser()
    c.commit()
    c.close()





if __name__ == '__main__':

    # this will run the first time the app is run
    if os.path.isfile(database) == False:
        from createdb import createDatabase
        createDatabase()

    insertUser()
