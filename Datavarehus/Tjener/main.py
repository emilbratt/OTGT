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

def getDates():
    c = connect()
    c.close()
    return None



def fetchData():

    c = connect()
    data['sales'] = c.sales()
    data['import'] = c.imports()
    data['soldout'] = c.soldout()
    c.close()
    print(data['sales'])
    print(data['import'])
    print(data['soldout'])




if __name__ == '__main__':
    data = {} # data fetched during execution is appended here
    fetchData()
    # getDates()
