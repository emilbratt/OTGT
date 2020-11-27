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
    sessionExecuteUpdate() is not finished
    byitemExecuteUpdate() is not finished
    send files to salesreport is not finished
'''

class Inventory:
    '''
        This class will create and read 4 individual files:
        1. byItem.json
        2. byShelf.json
        3. byTime.json
        4. current session file which is the most recent csv file by date and resides in
        ./inventory/sessions/YYYYMMDD.csv

        Methods:
        .sessionAdd('item barcode','shelf barcode')
            appends values to current session file in ./inventory/sessions/

        .inventoryAdd('item barcode','shelf barcode')
            adds values to the byItem.json, byShelf.json and byTime.json

        .inventoryDump()
            save byItem.json, byShelf.json and byTime.json

        .sessionExecuteUpdate()
            read all values from current session and update the sql database

        .wipeSessions()
            will wipe all session files (all files ending with .csv)

        .wipeInventory()
            will wipe the files in inventory (byItem.json, byShelf.json and byTime.json)

        .salesreportUpdate()
            send inventory files to host salesreport

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
        if self.debug['sql'] == True:
            try:
                import pyodbc # if sql is disabled, pyodbc will not be imported
            except ModuleNotFoundError:
                try:
                    call("echo", shell=True)
                    Log('pyodbc module was not found, shutting down', 1)
                    sleep(2)
                    call("sudo nohup shutdown -h now", shell=True)
                except NameError:
                    Log('pyodbc module was not found, exiting', 1)
                    exit()


        try:
            json_file = open('%s/byshelf.json'%self.file,encoding='utf-8')
            try:
                self.byshelf = json.load(json_file)
                Log('byshelf.json loaded succesfully')
                sleep(1.1)
            except json.decoder.JSONDecodeError:
                Log('JSONDecodeError on byshelf.json, shutting down')
                sleep(1.1)
                if self.debug == 'True':
                    exit()
                else:
                    call("sudo nohup shutdown -h now", shell=True)
            json_file.close()
        except FileNotFoundError:
            Log('byshelf.json file not found, creating new')
            sleep(1.1)
            self.byshelf = {}

        try:
            json_file = open('%s/byitem.json'%self.file,encoding='utf-8')
            try:
                self.byitem = json.load(json_file)
                Log('byitem.json loaded succesfully')
                sleep(1.1)
            except json.decoder.JSONDecodeError:
                Log('JSONDecodeError on byitem.json')
                sleep(1.1)
                if self.debug == 'True':
                    exit()
                else:
                    call("sudo nohup shutdown -h now", shell=True)
            json_file.close()
        except FileNotFoundError:
            Log('byitem.json file not found, creating new')
            sleep(1.1)
            self.byitem = {}


        try:
            json_file = open('%s/byTime.json'%self.file,encoding='utf-8')
            try:
                self.byTime = json.load(json_file)
                Log('byTime.json loaded succesfully')
                sleep(1.1)
            except json.decoder.JSONDecodeError:
                Log('JSONDecodeError on byTime.json')
                sleep(1.1)
                if self.debug == 'True':
                    exit()
                else:
                    call("sudo nohup shutdown -h now", shell=True)
            json_file.close()
        except FileNotFoundError:
            Log('byTime.json file not found, creating new')
            sleep(1.1)
            self.byTime = {}


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

            Log('reading values from ' + self.intDate + '.csv')
            with open('%s.csv' % self.sessionPath,'r') as csvfile:
                reader = csv.reader(csvfile)
                Log('updating database '
                + sqlCredentials['database'] + ' at '
                + sqlCredentials['server'])
                for row in reader:
                    print(row[0],row[1])

            # power off
            try:
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

    def inventoryDump(self):
        Log('running inventoryDump')
        with open('%s/byitem.json'%self.file,
        'w',encoding='utf-8') as json_file:
            json.dump(self.byitem, json_file, indent=2)

        with open('%s/byTime.json'%self.file,
        'w',encoding='utf-8') as json_file:
            json.dump(self.byTime, json_file, indent=2)

        with open('%s/byshelf.json'%self.file,
        'w',encoding='utf-8') as json_file:
            json.dump(self.byshelf, json_file, indent=2)


    def inventoryAdd(self, item, shelf):
        if item not in self.byitem:
            self.byitem.setdefault(item, [])
        if shelf not in self.byitem[item]:
            self.byitem.setdefault(item, []).append(shelf)

        if shelf not in self.byshelf:
            self.byshelf.setdefault(shelf, [])
        if item not in self.byshelf[shelf]:
            self.byshelf.setdefault(shelf, []).append(item)

        if item not in self.byTime:
            self.byTime[item] = {shelf:self.timestamp}
        else:
            self.byTime[item].update({shelf:self.timestamp})


    # update only newest shelf values with sql using the byitem.json
    def byitemExecuteUpdate(self, sqlCredentials):
        '''
            read values from byitem and update item and the newest shelf value
        '''

        if self.debug['sql'] == False:
            Log('sql is not activated, skipping update and exiting', 2)
            return None
        Log('executing byitemExecuteUpdate')
        Log('updating from inventory byitem.json to database '
        + sqlCredentials['database'] + ' at '
        + sqlCredentials['server'])


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

            Log(f'reading values from {self.file}/byitem.json.csv')
            for key in self.byitem:
                print(f'item {key} shelf {self.byitem[key][-1]}')
                # the last index represent the latest shelf value

            # power off
            try:
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


        # power off after update
        try:
            call("echo", shell=True)
            Log('powering off', 5)
            sleep(2)
            call("sudo nohup shutdown -h now", shell=True)
        except NameError:
            Log('exiting', 5)
            exit()


    def salesreportUpdate(self):
        '''
            for sending session files and logs to salesreport server
        '''
        pass


    # this will overwrite existing data with an empty dataset
    def wipeInventory(self):
        Log('wiping byitem, byshelf and byTime')
        json_file = open('%s/byitem.json'%self.file, 'w',encoding='utf-8')
        json.dump({}, json_file, indent=2)
        json_file.close()
        json_file = open('%s/byshelf.json'%self.file, 'w',encoding='utf-8')
        json.dump({}, json_file, indent=2)
        json_file.close()
        json_file = open('%s/byTime.json'%self.file, 'w',encoding='utf-8')
        json.dump({}, json_file, indent=2)
        json_file.close()


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
