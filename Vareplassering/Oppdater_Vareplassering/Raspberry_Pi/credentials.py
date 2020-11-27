#!/usr/bin/env python3
from subprocess import call
from time import sleep
import os
import json
from logging import Log

'''
    you can run this file directly to add parameters to credentials file
'''

# load credentials
def loadCredentials():
    mode = open('%s/debug.json'%
    os.path.dirname(os.path.realpath(__file__)),
    encoding='utf-8')
    debug = json.load(mode)
    mode.close()
    try:
        json_file = open('%s/credentials.json'%
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        encoding='utf-8')
        try:
            credentials = json.load(json_file)
            Log('credentials.json loaded succesfully')
            sleep(1.1)
        except AttributeError:
            Log('AttributeError on credentials.json, shutting down')
            sleep(1.1)
            # exit()
            call("sudo nohup shutdown -h now", shell=True)
        except json.decoder.JSONDecodeError:
            Log('json.decoder.JSONDecodeError on credentials.json, shutting down')
            sleep(1.1)
            # exit()
            call("sudo nohup shutdown -h now", shell=True)
        json_file.close()
    except FileNotFoundError:
        Log('credentials.json file not found, shutting down')
        sleep(1.1)
        call("sudo nohup shutdown -h now", shell=True)

    for key in credentials:
        if key == 'password':
            if debug['passwordhide'] == True:
                continue
            else:
                Log(key.ljust(10) + credentials[key].ljust(16))
        else:
            Log(key.ljust(10) + credentials[key].ljust(16))

    return credentials

# runs if flag credentials is applied
def createCredentials():

    credentials = {}
    attributeNames = ['server','port','database','user','password']
    for i in attributeNames:
        value = input(i+': ')
        credentials[i] = value
    input(attributeNames)
    input(credentials)
    json_file = open('%s/credentials.json'%os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'w',encoding='utf-8')
    json.dump(credentials, json_file, indent=2)
    json_file.close()
    for key in credentials:
        if key == 'password':
            continue
        else:
            Log(key.ljust(10) + credentials[key].ljust(16))

if __name__ == '__main__':
    Log(f'executing {__file__}')
    Log('Creating new credentials')
    createCredentials()
    Log('New credentials was stored')
