#!/usr/bin/env python3

import sys
import requests
import configparser
import os
import json

ENVIRONMENT_FILE = '../../../environment.ini'
if not os.path.isfile(ENVIRONMENT_FILE):
    exit('could not locate environment.ini stored in var ENVIRONMENT_FILE')

config = configparser.ConfigParser()
config.sections()
config.read(ENVIRONMENT_FILE)
URL = config['datawarehouse']['datawarehouse_ip'].strip('"')
PORT = config['datawarehouse']['cip_info_port'].strip('"')
URL = 'http' + '://' + URL + ':' + PORT + '/'

def get (QUERY):
    r = requests.get(URL + QUERY)
    print('GET request: ' + r.url)
    print('Response: ' + str(r.status_code))
    print('Response Headers')
    print(json.dumps(dict(r.request.headers), indent = 4))
    print(json.dumps(r.json(), indent=4, sort_keys=True))

def post (QUERY, DATA):
    r = requests.post(URL + QUERY, data=DATA)
    print('POST request: ' + r.url)
    print('Response: ' + str(r.status_code))
    print('Response Headers')
    print(json.dumps(dict(r.request.headers), indent = 4))
    print(json.dumps(r.json(), indent=4, sort_keys=True))

def put (QUERY, DATA):
    r = requests.put(URL + QUERY, data=DATA)
    print('POST request: ' + r.url)
    print('Response: ' + str(r.status_code))
    print('Response Headers')
    print(json.dumps(dict(r.request.headers), indent = 4))
    print(json.dumps(r.json(), indent=4, sort_keys=True))


if __name__ == '__main__':
    post('api/placement/v0/update_by_article_id', {'article_id': '10', 'shelf': 'a-a-3'})
