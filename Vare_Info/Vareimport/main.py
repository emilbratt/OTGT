#!/usr/bin/env python3
import os
import sys
import csv
from dbclient import *
from prettyquery import prettysql



def printTerminal():
    c = connect()
    data = c.getAllToday()
    c.close()
    for row in prettysql(data):
        print(row)


if __name__ == '__main__':
    # set working directory
    appRootPath = os.path.dirname(os.path.realpath(__file__))

    os.makedirs('%s/importert' % appRootPath, exist_ok=True)

    printTerminal()





'''notat
# for opening folder/file, fetched from (generer strekkoder)
if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    os.system('xdg-open "%s"' % os.path.join(path, "CSV"))
elif sys.platform.startswith('win32'):
    subprocess.Popen('explorer "%s"' % os.path.join(path, "CSV"))
'''
