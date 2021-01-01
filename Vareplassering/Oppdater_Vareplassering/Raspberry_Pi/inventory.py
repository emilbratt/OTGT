#!/usr/bin/env python3
from time import sleep
import csv
import sys
from datetime import datetime
import os
import json
# local modules
from writelog import Log
from credentials import loadCredentials


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
        # self.timestamp = self.getTime.strftime(
        #     "%Y-%m-%d_%H:%M:%S.%f")[:-4]

        self.file = os.path.join(
        os.path.dirname(os.path.realpath(
            __file__)), 'inventory')

        self.sessionPath = os.path.join(
        os.path.dirname(os.path.realpath(
            __file__)), 'inventory/sessions', self.intDate)

        # if no session file, touch to create empty
        self.sessionFile = os.path.join(self.sessionPath+'.csv')
        if not os.path.isfile(self.sessionFile):
            Log('First session run, creating session: ' + self.intDate)
            with open(self.sessionFile, 'a'):
                os.utime(self.sessionFile, None)


        with open('%s/debug.json'%os.path.join(
        os.path.dirname(os.path.realpath(__file__))), 'r') as mode:
            self.debug = json.load(mode)
        if self.debug['shutdown'] == True:
            from subprocess import call


        # load credentials for get server
        self.credentialsGet = loadCredentials('get')
        # load credentials for post server
        self.credentialsPost = loadCredentials('post')

        # read, add, save session csv
        self.sessions = [file for file
        in os.listdir('%s/inventory/sessions'%
        os.path.dirname(os.path.realpath(__file__)))
        if os.path.splitext(file)[-1] == '.csv']

        # check for existing sessions
        if self.sessions == []:
            Log('sessions directory /inventory/sessions/ is empty'
            + ', new session with stamp '
            + self.intDate + '.csv will be created')
            open(r'%s.csv' % self.sessionPath,'a', newline='')
        else:
            if int(self.intDate) < int(max(self.sessions)[0:8]):
                Log('datestamp: ' + self.intDate +
                ' is not up to date compared to latest session file')
            else:
                Log('session'.ljust(10) + self.intDate)


    def sessionAdd(self, item, shelf):
        # print(f'\tItem {item} Shelf {shelf}')
        with open(r'%s.csv' % self.sessionPath,'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
            item,shelf,datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")[:-4]
            ])

    # read from session file (csv) and update all values with sql
    def sessionExecuteUpdate(self):
        '''
            read all values from current session
            and run queries to update the sql server
        '''

        # if sql is disabled, pyodbc and mariadb will not be imported
        if self.debug['sql'] == True:
            try:
                 import pyodbc
            except ModuleNotFoundError:
                Log('pyodbc module was not found', 1)
                if self.debug['shutdown'] == True:
                    from subprocess import call
                try:
                    call("echo", shell=True) # will trigger exception of error
                    sleep(2)
                    call("sudo nohup shutdown -h now", shell=True)
                except NameError:
                    exit()
            try:
                 import mariadb
            except ModuleNotFoundError:
                Log('mariadb module was not found', 1)
                if self.debug['shutdown'] == True:
                    from subprocess import call
                try:
                    call("echo", shell=True) # will trigger exception of error
                    sleep(2)
                    call("sudo nohup shutdown -h now", shell=True)
                except NameError:
                    return None


        Log('executing sessionExecuteUpdate')
        if self.debug['sql'] == False:
            Log('sql is not activated, skipping update', 2)
            return None


        # connect to store
        try:
            cnxnGet = pyodbc.connect(
            'DRIVER={FreeTDS};SERVER=%s;PORT=%s;DATABASE=%s;UID=%s;PWD=%s' %(
                self.credentialsGet['server'],
                self.credentialsGet['port'],
                self.credentialsGet['database'],
                self.credentialsGet['user'],
                self.credentialsGet['password']
                )
            )
            Log('Get database connected succesfully')
            cursorGet = cnxnGet.cursor()
        except pyodbc.OperationalError:
            Log('Get database connection failed with pyodbc.OperationalError', 1)
            return None

        # connect to data warehouse
        try:
            cnxnPost = mariadb.connect(
                user=self.credentialsPost['user'],
                password=self.credentialsPost['password'],
                host=self.credentialsPost['server'],
                port=int(self.credentialsPost['port']),
                database=self.credentialsPost['database']
            )
            Log('Post database connection succesfully')
            cursorPost = cnxnPost.cursor()
        except mariadb.Error:
            Log('Post database connection failed with mariadb.Error', 1)
            return None


        articleIdGet = '''
        SELECT
            Article.articleId
        FROM
            ArticleEAN
        INNER JOIN
            Article
        ON
            ArticleEAN.articleId = Article.articleId
        WHERE
            ArticleEAN.eanCode = (?)

        '''

        updateShelfGet = '''
        UPDATE
            articleStock
        SET
            StorageShelf =(?)
        FROM
            articleStock
        JOIN
            ArticleEAN
        ON
            articleStock.articleId = ArticleEAN.articleId
        WHERE
            ArticleEAN.eanCode=(?)'''


        deDuplicate = []
        preparePost = []
        Log('reading values from ' + self.intDate + '.csv')
        with open('%s.csv' % self.sessionPath,'r') as csvfile:
            reader = csv.reader(csvfile)
            Log('updating database '
            + self.credentialsGet['database'] + ' at '
            + self.credentialsGet['server'])
            for row in reader:
                if [row[0],row[1]] not in deDuplicate:
                    deDuplicate.append([row[0],row[1]])

                    # append rows with timestamp and date for data warehouse
                    add = cursorGet.execute(articleIdGet, row[0]).fetchone()
                    prep = []
                    if add != None:
                        prep.append(add[0])
                        prep.append(row[1])
                        prep.append(row[2])
                        prep.append(int(self.intDate))
                        preparePost.append(prep)

                    # append to store
                    print(f'Updating shelf for {row[0]} to {row[1]}')
                    cursorGet.execute(updateShelfGet, row[1], row[0])
                    cnxnGet.commit()
                    sleep(0.2)


        cursorGet.close()
        cnxnGet.close()

        # update data warehouse

        # get list to compare
        selectShelfPost = '''
        SELECT *
        FROM `placement`
        WHERE yyyymmdd = (?);
        '''
        selectShelf = cursorPost.execute(selectShelfPost,(self.intDate,))
        result = cursorPost.fetchall()
        for row in result:
            if list(row) in preparePost:
                preparePost.remove(list(row))

        # after comparison, insert new distinct values
        insertShelfPost = '''
        INSERT INTO `placement`
            (article_id, stock_location, timestamp,yyyymmdd)
        VALUES
            (?, ?, ?, ?);
        '''
        if preparePost != []:
            cursorPost.executemany(insertShelfPost,preparePost)
            cnxnPost.commit()
        cnxnPost.close()

        if self.debug['live'] == True:
            Log('Finish updating, live mode = True -> keep running', 5)
            return None

        # power off if enabled or exit if not
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


    def wipeSessions(self):
        allSessions = [f for f
        in os.listdir('%s/inventory/sessions'%
        os.path.dirname(os.path.realpath(__file__)))
        if os.path.splitext(f)[-1] == '.csv']
        for session in allSessions:
            Log('deleting ' + session + ' from ./inventory/sessions/','2')
            os.remove(os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            'inventory', 'sessions',session))
