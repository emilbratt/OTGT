#!/usr/bin/env python3
import os
import sys
import csv
from dataget import *
from datapost import *
from datetime import datetime
import json

'''
    flags: daily, weekly, monthly

    daily = fetches only daily report
    weekly = fetches daily and weekly report
    monthly = fetches daily, weekly and monthly report
'''

# get timestamp and date
timestamp = datetime.now()
ymd = timestamp.strftime("%Y-%m-%d")

# load mode
mode = open('%s/mode.json'%
os.path.dirname(os.path.realpath(__file__)),
encoding='utf-8')
runMode = json.load(mode)
mode.close()



# set working directory
dirs = {}
dirs['App'] = os.path.dirname(os.path.realpath(__file__))
dirs['Data'] = os.path.join(dirs['App'], 'Data')
dirs['Utsolgt'] = os.path.join(dirs['App'], 'Data','Utsolgt')
dirs['Import'] = os.path.join(dirs['App'], 'Data', 'Import')
dirs['Omsetning'] = os.path.join(dirs['App'], 'Data', 'Omsetning')

# if no dir, create new
os.makedirs(dirs['Data'], exist_ok=True)
os.makedirs(dirs['Utsolgt'], exist_ok=True)
os.makedirs(dirs['Import'], exist_ok=True)
os.makedirs(dirs['Omsetning'], exist_ok=True)
os.makedirs(dirs['Utsolgt'], exist_ok=True)
for dir in dirs:
    if dir != 'Data' and dir != 'App':
        os.makedirs(dirs[dir]+'/Daglig', exist_ok=True)
        os.makedirs(dirs[dir]+'/Ukentlig', exist_ok=True)
        os.makedirs(dirs[dir]+'/Maanedlig', exist_ok=True)



def writeSpreadsheet(data: dict):
    import openpyxl
    from openpyxl import Workbook
    from openpyxl.utils import get_column_letter
    from openpyxl.styles import Alignment


    def cloudUpload(fileName):
        pass

    def exportXLSX(fileName: str):

        # load spreadsheet
        wb = Workbook()
        ws = wb.active

        # apply default col length
        cellLength = {}
        for i in range(7):
            cellLength[i] = 5

        # set length of col based on length of longest cell value
        for row in data[category][when]:
            for i,cell in enumerate(row):
                if i not in cellLength:
                    cellLength[i] = 1
                try:
                    if cellLength[i] < len(str(cell)):
                        cellLength[i] = len(str(cell))
                except KeyError:
                    continue

        ws.column_dimensions['A'].width = cellLength[0]+5
        ws.column_dimensions['B'].width = cellLength[1]+5
        ws.column_dimensions['C'].width = cellLength[2]+5
        ws.column_dimensions['D'].width = cellLength[3]+5
        ws.column_dimensions['E'].width = cellLength[4]+5
        ws.column_dimensions['F'].width = cellLength[5]+5
        ws.column_dimensions['G'].width = cellLength[6]+5

        for row in data[category][when]: # append rows to spreadsheet
            ws.append(list(row))

        for col in ws.columns: # align all fields with value to center
            for cell in col:
                cell.alignment = Alignment(horizontal='center', vertical='center')




        # save spreadsheet
        wb.save(fileName)

    for category in data:
        if category != 'Tider':
            for when in data[category]:
                fileName = os.path.join(dirs[category],when,data['Tider']['yesterday']['YYYYMMDD']+'.xlsx')
                exportXLSX(fileName)
                # cloudUpload(fileName)



def updateCIP(data: dict):
    '''
        sends the recorded data to mariadb -> CIP on salesreport
    '''
    pass


def fetchDaily():
    data = {}
    c = Getrecords()
    data['Tider'] = c.fetchTime()
    data['Omsetning'] = {'Daglig':c.turnoverYesterday()}
    data['Import'] = {'Daglig':c.importsYesterdayy()}
    data['Utsolgt'] = {'Daglig':c.soldoutYesterdayy()}

    updateCIP(data)

    colName = [
    'Totalt','00-01','01-02','02-03','03-04','04-05','05-06','06-07','07-08',
    '08-09','09-10','10-11','11-12','12-13','13-14','14-15','15-16','16-17',
    '17-18','18-19','19-20','20-21','21-22','22-23','23-24'
    ]
    data['Omsetning']['Daglig'].insert(0,colName)
    data['Omsetning']['Daglig'].insert(0,['Omsetning'])
    data['Omsetning']['Daglig'].insert(0,[data['Tider']['yesterday']['human']])
    data['Omsetning']['Daglig'].insert(0,[data['Tider']['yesterday']['weekday'].title() +' Uke-' + data['Tider']['yesterday']['weekNum']])




    colName = [
    'Artikkel ID','Merke','Navn',
    'Importert','Antall Lager','Lagerplass','Lev.ID'
    ]
    data['Import']['Daglig'].insert(0,colName)
    data['Import']['Daglig'].insert(0,['Vareimport'])
    data['Import']['Daglig'].insert(0,[data['Tider']['yesterday']['human']])
    data['Import']['Daglig'].insert(0,[data['Tider']['yesterday']['weekday'].title() +' Uke-' + data['Tider']['yesterday']['weekNum']])
    if len(data['Import']['Daglig']) < 5: # less than 5 rows means no records from this query
        data['Import']['Daglig'][2] = ['Ingen Importerte Varer I Dag']
        del data['Import']['Daglig'][3]






    colName = [
    'Artikkel ID','Merke','Navn','Antall Lager',
    'Lagerplass','Sist Importert','Lev. ID'
    ]


    data['Utsolgt']['Daglig'].insert(0,colName)
    data['Utsolgt']['Daglig'].insert(0,['Utsolgte Varer'])
    data['Utsolgt']['Daglig'].insert(0,[data['Tider']['yesterday']['human']])
    data['Utsolgt']['Daglig'].insert(0,[data['Tider']['yesterday']['weekday'].title() +' Uke-' + data['Tider']['yesterday']['weekNum']])
    if len(data['Utsolgt']['Daglig']) < 5: # less than 5 rows means no records from this query
        data['Utsolgt']['Daglig'][2] = ['Ingen Utsolgte Varer I Dag']
        del data['Utsolgt']['Daglig'][3]

    c.close()

    writeSpreadsheet(data)



def fetchWeekly():
    # data = {}
    # c = connect()
    # data['Tider'] = c.fetchTime()
    # data['Omsetning'] = {'Daglig':c.turnoverYesterday()}
    # data['Import'] = {'Daglig':c.importsYesterdayy()}
    # data['Utsolgt'] = {'Daglig':c.soldoutYesterdayy()}
    # c.close()
    # print(data['Omsetning'])
    #
    # writeSpreadsheet(data)
    # writeSQL(data)
    pass




if __name__ == '__main__':
    if len(sys.argv) > 1:
        pass
    data = {} # data fetched during execution is appended here
    fetchDaily()
    # fetchWeekly()
