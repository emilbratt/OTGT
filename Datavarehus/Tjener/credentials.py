#!/usr/bin/env python3
from subprocess import call
from time import sleep
import os
import json
from writelog import Log

'''
    you can run this file directly to add new credentials
'''

# load credentials
def loadCredentials(db):
    try:
        json_file = open('%s/credentials.json'%
            os.path.dirname(os.path.realpath(__file__)),
            encoding='utf-8')
        try:
            credentials = json.load(json_file)
            Log('credentials.json loaded succesfully','noprint')
            sleep(1.1)
        except AttributeError:
            Log('AttributeError on credentials.json, exiting')
            sleep(1.1)

            exit()
        except json.decoder.JSONDecodeError:
            Log('json.decoder.JSONDecodeError on credentials.json, exiting')
            sleep(1.1)

            exit()
        json_file.close()
    except FileNotFoundError:
        Log('credentials.json file not found, exiting')
        sleep(1.1)
        exit()

    for key in credentials[db]:
        if key == 'password':
            continue
        else:
            Log(key.ljust(10) + credentials[db][key].ljust(16),'noprint')

    return credentials[db]


def createCredentials():


    try:
        json_file = open('%s/credentials.json'%
            os.path.dirname(os.path.realpath(__file__)),
            encoding='utf-8')
        try:
            credentials = json.load(json_file)
            Log('credentials.json loaded succesfully','noprint')
            sleep(1.1)
        except AttributeError:
            Log('AttributeError on credentials.json, exiting')
            sleep(1.1)

            exit()
        except json.decoder.JSONDecodeError:
            Log('json.decoder.JSONDecodeError on credentials.json, exiting')
            sleep(1.1)

            exit()
        json_file.close()
    except FileNotFoundError:
        Log('credentials.json file not found, creating new')
        credentials = {}
        sleep(1.1)


    print('\t1. For Post\n\t2. For Get\n\t3. For Cloud')
    db = input()

    if db == '1':
        db = 'post'
        credentials['post'] = {}
    elif db == '2':
        db = 'get'
        credentials['get'] = {}
    elif db == '3':
        db = 'cloud'
        credentials['cloud'] = {}
    else:
        exit()


    databaseAttributes = ['server','port','database','user','password']
    cloudAttributes = ['server','user','password']
    inputAccept = False
    if db == 'post' or db == 'get':
        while inputAccept == False:
            for i in databaseAttributes:
                value = input(i+': ')
                credentials[db][i] = value
            isOK = input('is this correct?\n1. yes\n2.no\ntype: ')
            if isOK == '1':
                inputAccept = True
    if db == 'cloud':
        while inputAccept == False:
            for i in cloudAttributes:
                value = input(i+': ')
                credentials[db][i] = value
            isOK = input('is this correct?\n1. yes\n2.no\ntype: ')
            if isOK == '1':
                inputAccept = True

    json_file = open('%s/credentials.json'%
        os.path.dirname(os.path.realpath(__file__)),
        'w',encoding='utf-8')
    json.dump(credentials, json_file, indent=2)
    json_file.close()
    for key in credentials[db]:
        if key == 'password':
            continue
        else:
            Log(key.ljust(10) + credentials[db][key].ljust(16),'noprint')


if __name__ == '__main__':
    Log(f'executing {__file__}')
    Log('Creating new credentials')
    createCredentials()
    Log('New credentials was stored')
