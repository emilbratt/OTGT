import os, sys
def loadDriver():
    if sys.platform.startswith('linux'):
        return {'linux':'FreeTDS'}
    elif sys.platform.startswith('win32'):
        return {'windows':'ODBC Driver 17 for SQL Server'}
    elif sys.platform.startswith('darwin'):
        # dont support mac, yet
        exit()
    else:
        # what the heck are you running?
        exit()
