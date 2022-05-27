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
    print('PUT request: ' + r.url)
    print('Response: ' + str(r.status_code))
    print('Response Headers')
    print(json.dumps(dict(r.request.headers), indent = 4))
    print(json.dumps(r.json(), indent=4, sort_keys=True))

def delete (QUERY):
    r = requests.delete(URL + QUERY)
    print('DELETE request: ' + r.url)
    print('Response: ' + str(r.status_code))
    print('Response Headers')
    print(json.dumps(dict(r.request.headers), indent = 4))
    print(json.dumps(r.json(), indent=4, sort_keys=True))


if __name__ == '__main__':
    # get('api/article/v0/get_article_id/5712396000612')
    # post('api/placement/v0/update_by_article_id', {'article_id': '10', 'shelf': 'a-a-3'})
    delete('api/instructions/v0/delete/bygg/varme_styring.pdf')
