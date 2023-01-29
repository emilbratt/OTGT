import sqlite3

class Entities:
    def __init__(self, databasefile: str):
         self.databasefile = databasefile

    def elspot(self):
        cnxn = sqlite3.connect(self.databasefile)
        from .elspot import Operation
        return Operation(cnxn)
