import sqlite3
import os

class Jobs:

    def __init__(self):
        print('this is Jobs')
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.home = os.path. expanduser('~')
        print(self.home)
        print(self.cwd)
