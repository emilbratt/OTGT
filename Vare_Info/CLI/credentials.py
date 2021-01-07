#!/usr/bin/env python3
from subprocess import call
from time import sleep
import os
import json
from writelog import Log

'''
    you can run this file directly to add new credentials
'''

appPath = os.path.dirname(os.path.realpath(__file__))
modePath = os.path.join(appPath, 'mode.json')
credPath = os.path.join(appPath, 'credentials.json')


# load credentials
def loadCredentials():
    modeFile = open(modePath,  encoding='utf-8')
    mode = json.load(modeFile)
    modeFile.close()
    try:
        credFile = open(credPath, encoding='utf-8')
        try:
            credentials = json.load(credFile)
            Log('credentials.json loaded succesfully','noprint')
            sleep(1.1)
        except AttributeError:
            Log('AttributeError on credentials.json, shutting down')
            sleep(1.1)

            call("sudo nohup shutdown -h now", shell=True)
        except json.decoder.JSONDecodeError:
            Log('json.decoder.JSONDecodeError on credentials.json, shutting down')
            sleep(1.1)

            call("sudo nohup shutdown -h now", shell=True)
        credFile.close()
    except FileNotFoundError:
        Log('credentials.json file not found, shutting down')
        sleep(1.1)
        call("sudo nohup shutdown -h now", shell=True)

    for key in credentials:
        if key == 'password':
            if mode['passwordhide'] == True:
                continue
            else:
                Log(key.ljust(10) + credentials[key].ljust(16),'noprint')
        else:
            Log(key.ljust(10) + credentials[key].ljust(16),'noprint')

    return credentials


def createCredentials():
    credentials = {}
    attributeNames = ['server','port','database','user','password']
    inputAccept = False
    while inputAccept == False:
        for i in attributeNames:
            value = input(i+': ')
            credentials[i] = value
        isOK = input('is this correct?\n1. yes\n2.no\ntype: ')
        if isOK == '1':
            inputAccept = True

    credFile = open(credPath, 'w',encoding='utf-8')
    json.dump(credentials, credFile, indent=2)
    credFile.close()
    for key in credentials:
        if key == 'password':
            continue
        else:
            Log(key.ljust(10) + credentials[key].ljust(16),'noprint')


if __name__ == '__main__':
    Log(f'executing {__file__}')
    Log('Creating new credentials')
    createCredentials()
    Log('New credentials was stored')
