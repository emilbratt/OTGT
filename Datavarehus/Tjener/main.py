#!/usr/bin/env python3
import os
import sys
import csv
from dbclient import *
from datetime import datetime

# create a clear screen function
clearScreen = lambda : os.system(
    'cls' if os.name == 'nt' else 'clear')

# get timestamp and date
timestamp = datetime.now()
ymd = timestamp.strftime("%Y-%m-%d")

# set working directory
filePath = os.path.dirname(os.path.realpath(__file__))
pathData = os.path.join(filePath, 'Data')
pathSalg = os.path.join(filePath, 'Data','Salg')
pathImport = os.path.join(filePath, 'Data', 'Import')
pathOmsetning = os.path.join(filePath, 'Data', 'Omsetning')

# if no dir, create new
os.makedirs(pathData, exist_ok=True)
os.makedirs(pathSalg, exist_ok=True)
os.makedirs(pathImport, exist_ok=True)
os.makedirs(pathOmsetning, exist_ok=True)



def writeSpreadsheet(data):
    pass


def fetchYesterday():

    c = connect()
    times = c.fetchTime()
    turnoverYesterday = c.turnoverYesterday()
    importsYesterdayy = c.importsYesterdayy()
    soldoutYesterdayy = c.soldoutYesterdayy()
    c.close()
    for row in turnoverYesterday:
        print(row)
    print()
    for row in importsYesterdayy:
        print(row)
    print()
    for row in soldoutYesterdayy:
        print(row)

if __name__ == '__main__':
    data = {} # data fetched during execution is appended here
    fetchYesterday()
    # getDates()
