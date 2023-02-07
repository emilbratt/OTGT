import sqlite3

class Tables:
    def __init__(self, databasefile: str):
         self.databasefile = databasefile

    def elspot(self):
        cnxn = sqlite3.connect(self.databasefile)
        from .elspot import Operation
        return Operation(cnxn)

    def plot(self):
        cnxn = sqlite3.connect(self.databasefile)
        from .plot import Operation
        return Operation(cnxn)
