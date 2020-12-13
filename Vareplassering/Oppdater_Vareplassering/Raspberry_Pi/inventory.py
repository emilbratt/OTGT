#!/usr/bin/env python3
from time import sleep
import csv
import sys
from datetime import datetime
import os
import json
from logging import Log

'''
    notes:
    send files to salesreport is not finished
'''

class Inventory:
    '''
        This class will create a session file:
        The current session file which is the most recent csv file by date and resides in
        ./inventory/sessions/YYYYMMDD.csv

        Methods:
        .sessionAdd('item barcode','shelf barcode','timestamp')
            appends values to current session file in ./inventory/sessions/

        .sessionExecuteUpdate()
            read all values from current session and update the sql database

        .wipeSessions()
            will wipe all session files (all files ending with .csv)

        .salesreportUpdate()
            send inventory files to host salesreport
            not finnished yet
    '''

    def __init__(self):
        os.makedirs('%s/inventory'%os.path.dirname(os.path.realpath(
        __file__)), exist_ok=True)

        os.makedirs('%s/inventory/sessions'%os.path.dirname(os.path.realpath(
        __file__)), exist_ok=True)

        self.getTime = datetime.now()
        self.intDate = self.getTime.strftime("%Y%m%d")
        self.timestamp = self.getTime.strftime(
        "%Y-%m-%d_%H:%M:%S.%f")[:-4]

        self.file = os.path.join(
        os.path.dirname(os.path.realpath(
        __file__)), 'inventory')

        self.sessionPath = os.path.join(
        os.path.dirname(os.path.realpath(
        __file__)), 'inventory/sessions', self.intDate)

        with open('%s/debug.json'%os.path.join(
        os.path.dirname(os.path.realpath(__file__))), 'r') as mode:
            self.debug = json.load(mode)
        if self.debug['shutdown'] == True:
            from subprocess import call



        # read, add, save session csv
        self.sessions = [file for file
        in os.listdir('%s/inventory/sessions'%
        os.path.dirname(os.path.realpath(__file__)))
        if os.path.splitext(file)[-1] == '.csv']

        # check for existing sessions
        if self.sessions == []:
            Log('no session files (csv) in .inventory/sessions/'
            + ', new session with stamp '
            + self.intDate + '.csv will be created')
            open(r'%s.csv' % self.sessionPath,'a', newline='')
        else:
            if int(self.intDate) < int(max(self.sessions)[0:8]):
                Log('datestamp: ' + self.intDate +
                ' is not up to date compared to latest session file')
            else:
                Log('session file: ' + self.intDate)


    def sessionAdd(self, item, shelf):
        # print(f'\tItem {item} Shelf {shelf}')
        with open(r'%s.csv' % self.sessionPath,'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([item,shelf,self.timestamp])

    # read from session file (csv) and update all values with sql
    def sessionExecuteUpdate(self, sqlCredentials):
        '''
            read all values from current session
            and run queries to update the sql server
        '''


        if self.debug['sql'] == True:
            try:
                import pyodbc # if sql is disabled, pyodbc will not be imported

            except ModuleNotFoundError:
                if self.debug['shutdown'] == True:
                    from subprocess import call
                try:
                    call("echo", shell=True)
                    Log('pyodbc module was not found, shutting down', 1)
                    sleep(2)
                    call("sudo nohup shutdown -h now", shell=True)
                except NameError:
                    Log('pyodbc module was not found, exiting', 1)
                    exit()


        Log('executing sessionExecuteUpdate')
        if self.debug['sql'] == False:
            Log('sql is not activated, skipping update and exiting', 2)
            return None

        try:
            cnxn = pyodbc.connect(
            'DRIVER={FreeTDS};SERVER=%s;PORT=%s;DATABASE=%s;UID=%s;PWD=%s' %(
                sqlCredentials['server'],
                sqlCredentials['port'],
                sqlCredentials['database'],
                sqlCredentials['user'],
                sqlCredentials['password']
                )
            )
            Log('sql database connected succesfully')
            cursor = cnxn.cursor()

            queryUpdateShelf = '''
            UPDATE articleStock
            SET StorageShelf =(?)
            FROM articleStock
            JOIN ArticleEAN ON articleStock.articleId = ArticleEAN.articleId
            WHERE ArticleEAN.eanCode=(?)'''

            Log('reading values from ' + self.intDate + '.csv')
            with open('%s.csv' % self.sessionPath,'r') as csvfile:
                reader = csv.reader(csvfile)
                Log('updating database '
                + sqlCredentials['database'] + ' at '
                + sqlCredentials['server'])
                for row in reader:
                    print('Updating')
                    print(row[0]) # barcode
                    print(row[1]) # shelf value

                    cursor.execute(queryUpdateShelf, row[1], row[0])
                    cnxn.commit()

                    sleep(0.4)
            cursor.close()
            cnxn.close()

            # power off
            try:
                if self.debug['shutdown'] == True:
                    from subprocess import call
                call("echo", shell=True)
                Log('powering off', 5)
                sleep(2)
                call("sudo nohup shutdown -h now", shell=True)
            except NameError:
                Log('exiting', 5)
                exit()
        except pyodbc.OperationalError:
            Log('sql database connection failed with pyodbc.OperationalError', 1)
            return None



    def salesreportUpdate(self):
        '''
            for sending session files and logs to salesreport server
        '''
        pass


    def wipeSessions(self):
        allSessions = [f for f
        in os.listdir('%s/inventory/sessions'%
        os.path.dirname(os.path.realpath(__file__)))
        if os.path.splitext(f)[-1] == '.csv']
        for i in allSessions:
            Log('deleting ' + i + ' from ./inventory/sessions/')
            os.remove(os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            'inventory', 'sessions',i))
