#!/usr/bin/env python3

import sys
import requests
import configparser
import os

ENVIRONMENT_FILE = '../../../environment.ini'
URL = False # base url to api which is loaded from environment.ini
PORT = False # for testing against developement environment
QUERY = False # value after url, for example: api/test/v01/hello
HTTP = False # contains either http or https
USE_TLS = False # will swap http with https

def get (URL):
    r = requests.get(URL)
    print('GET request: ' + r.url)
    print('Response: ' + str(r.status_code))
    print(r.json())
    print()

def post (URL, data):
    r = requests.post(URL, data)
    print('POST request: ' + r.url)
    print('Response: ' + str(r.status_code))
    print(r.json())
    print()

def put (URL, data):
    r = requests.put(URL, data)
    print('POST request: ' + r.url)
    print('Response: ' + str(r.status_code))
    print(r.json())
    # print(r.text())
    print()


if __name__ == '__main__':
    if not os.path.isfile(ENVIRONMENT_FILE):
        exit('could not locate environment.ini stored in var ENVIRONMENT_FILE')

    config = configparser.ConfigParser()
    config.sections()
    config.read(ENVIRONMENT_FILE)
    URL = config['datawarehouse']['datawarehouse_ip'].strip('"')
    PORT = config['datawarehouse']['cip_info_port'].strip('"')

    HTTP = 'http'
    if USE_TLS:
        HTTP = 'https'

    QUERY = 'api/placement/v0/update_by_article_id'
    URL = HTTP + '://' + URL + ':' + PORT + '/' + QUERY

    # get(URL)
    post(URL, {'article_id': '10', 'shelf': 'a-a-3'})
