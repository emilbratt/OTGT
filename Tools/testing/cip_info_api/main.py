#!/usr/bin/env python3

'''
    TODO:
        add..
            run from same directory as this script
            and pass arguments:
                1. api endpint (example: test/v01/hello)
                2. method
                3. data (if methid = post or put)
'''

import sys
import requests
import configparser
import os

ENVIRONMENT_FILE = '../../../environment.ini'
URL = False # base url to api which is loaded from environment.ini
PORT = False # for testing against developement environment
REDIRECT = False # value after url, for example: api/test/v01/hello
HTTP = False # contains either http or https
USE_TLS = False # will swap http with https


def get (URL):
    r = requests.get(URL)
    print('GET request: ' + r.url)
    print('Response: ' + str(r.status_code))
    r.status_code
    print(r.json())
    print()

def post (URL, data):
    r = requests.post(URL, data)
    print('POST request: ' + r.url)
    print('Response: ' + str(r.status_code))
    print(r.json())
    print()


if __name__ == '__main__':
    if not os.path.isfile(ENVIRONMENT_FILE):
        exit('could not locate environment.ini, current path is set: '
             + ENVIRONMENT_FILE)

    config = configparser.ConfigParser()
    config.sections()
    config.read(ENVIRONMENT_FILE)
    URL = config['datawarehouse']['server_ip'].strip('"')
    PORT = config['datawarehouse']['dev_port'].strip('"')
    if URL == False:
        exit('could not load [datawarehouse][server_ip] form environment')

    HTTP = 'http'
    if USE_TLS:
        HTTP = 'https'


    if len(sys.argv) == 1:
        REDIRECT = 'api/test/v0/hello'
        URL = HTTP + '://' + URL + ':' + PORT + '/' + REDIRECT

        get(URL)
        post(URL, {'foo': 'baaar'})
