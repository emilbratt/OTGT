#!/usr/bin/env python3
# Emil Bratt -> emilbratt@gmail.com
import os

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
    from createtables import createDatabase
    createDatabase()

# testing
from dbclient import connect
c = connect()
c.insertRoles()
c.commit()
c.printRoles()
