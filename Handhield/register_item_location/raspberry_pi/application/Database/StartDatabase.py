import sqlite3
import os.path as path

# if database file does not exist, this script will create it and its tables

class CreateTables:

    def __init__(self):
        print('this is CreateTables')
        self.dir = path.dirname(path.realpath(__file__))
        self.db = path.join(self.dir, 'data.sqlite')
        if not path.isfile(path.join(self.dir, 'data.sqlite')):
            self.create_tables()

        # self.con = sqlite3.connect('example.db')
        # self.cur = self.con.cursor()

    def create_tables(self):
        print('create table..')
