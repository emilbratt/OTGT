#!/usr/bin/env python3
import os
import sys
import csv
import json
from dataget import Getconnect
from datapost import Postconnect
from datetime import datetime
from writelog import Log

'''
    notes:
    uncomment create writeSpreadsheet
'''
'''
    flags: daily, weekly, monthly

    daily = fetches only daily report
    weekly = fetches daily and weekly report
    monthly = fetches daily, weekly and monthly report
'''

# get timestamp and date
timestamp = datetime.now()
ymd = timestamp.strftime("%Y-%m-%d")


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



def initialize():
    # get highest id number for article id and brand id
    c = Postconnect()
    brand_idMax = c.brandsGetMax()
    article_idMax = c.articlesGetMax()
    c.close()

    # fetch new records from retial
    c = Getconnect()
    brandsRes = []
    for row in c.getBrands(brand_idMax):
        brandsRes.append(tuple(row))
    articlesRes = []
    for row in c.getArticles(article_idMax):
        articlesRes.append(tuple(row))
    c.close()

    # insert records into datawarehouse
    c = Postconnect()
    if brandsRes != []:
        Log(f'Updating brands from brand_id: {brand_idMax}', 'noprint')
        c.brandsPost(brandsRes)
    if articlesRes != []:
        Log(f'Updating articles from article_id: {article_idMax}', 'noprint')
        c.articlesPost(articlesRes)
    c.close()




def getRecords():
    c = Getconnect()
    data['Tider'] = c.fetchTime()
    data['Omsetning'] = {'Daglig':c.turnoverYesterday()}
    data['Import'] = {'Daglig':c.importsYesterdayy()}
    data['Utsolgt'] = {'Daglig':c.soldoutYesterdayy()}
    c.close()



def updateCIP():
    # format dates for columns in data warehouse
    dateInsert = []
    dateInsert.append(int(data['Tider']['yesterday']['YYYYMMDD'][:4]))
    dateInsert.append(int(data['Tider']['yesterday']['YYYYMMDD'][4:6]))
    dateInsert.append(int(data['Tider']['yesterday']['YYYYMMDD'][6:8]))
    dateInsert.append(int(data['Tider']['yesterday']['weekNum']))
    dateInsert.append(data['Tider']['yesterday']['weekday'])
    dateInsert.append(int(data['Tider']['yesterday']['YYYYMMDD']))
    dateInsert.append(data['Tider']['yesterday']['human'])


    def prepareRecords(row,category):
        if category == 'Omsetning':
            turnover = {}
            # extract hourly values and add dates
            turnover['timer'] = [v for v in row[1:]]
            for value in dateInsert:
                turnover['timer'].append(value)
            # extract total value and dates
            turnover['dag'] = [row[0]]
            for value in dateInsert:
                turnover['dag'].append(value)
            return turnover

        elif category == 'Utsolgt' or category == 'Import':
            for value in dateInsert:
                row.append(value)
            return row
        else:
            return None


    prepared = {}
    for category in data:
        if category != 'Tider':
            for when in data[category]:
                if when == 'Daglig':
                    prepared[category] = [] # add category as key
                    # prepare rows with additional data
                    for row in data[category][when]:
                        prepared[category].append(
                            prepareRecords(
                                list(row),category
                            )
                        )


    c = Postconnect()
    c.soldoutPost(prepared['Utsolgt'])
    c.importsPost(prepared['Import'])
    c.turnover_hourlyPost(prepared['Omsetning'][0]['timer'])
    c.turnover_dailyPost(prepared['Omsetning'][0]['dag'])
    c.close()

def writeSpreadsheet():
    import openpyxl
    from openpyxl import Workbook
    from openpyxl.utils import get_column_letter
    from openpyxl.styles import Alignment

    def exportXLSX(fileName: str):

        def cloudUpload(fileName: str):
            pass

        # load spreadsheet
        wb = Workbook()
        ws = wb.active

        # apply default col length
        cellLength = {}
        for i in range(10):
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

        # apply col length from values in cellLength to cell A-J
        ws.column_dimensions['A'].width = cellLength[0]+5
        ws.column_dimensions['B'].width = cellLength[1]+5
        ws.column_dimensions['C'].width = cellLength[2]+5
        ws.column_dimensions['D'].width = cellLength[3]+5
        ws.column_dimensions['E'].width = cellLength[4]+5
        ws.column_dimensions['F'].width = cellLength[5]+5
        ws.column_dimensions['G'].width = cellLength[6]+5
        ws.column_dimensions['H'].width = cellLength[7]+5
        ws.column_dimensions['I'].width = cellLength[8]+5
        ws.column_dimensions['J'].width = cellLength[9]+5

        for row in data[category][when]: # append rows to spreadsheet
            ws.append(list(row))

        for col in ws.columns: # align all fields with value to center
            for cell in col:
                cell.alignment = Alignment(horizontal='center', vertical='center')

        # save spreadsheet
        wb.save(fileName)

        ''' note: remember to fix this '''
        cloudUpload(fileName) # note: add send wb to cloud


    # giv column names and add date info before exporting to spreadsheet

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

    # loop through results in data and export spreadsheet
    for category in data:
        if category != 'Tider':
            for when in data[category]:
                fileName = os.path.join(dirs[category],when,data['Tider']['yesterday']['YYYYMMDD']+'.xlsx')
                exportXLSX(fileName)










if __name__ == '__main__':


    data = {} # data fetched during execution is appended here
    initialize() # insert id_records in data warehouse if new data from store

    getRecords() # populate the data dict with new data from the store
    updateCIP() # send the newly populated data and insert into data warehouse
    writeSpreadsheet() # export spreadsheets from the data
