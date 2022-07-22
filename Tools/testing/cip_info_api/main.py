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

def print_response (r):
    method = str(r.request).split()[1]
    print(method + ' ' + r.url)
    print('Response Code: ' + str(r.status_code))
    print('Response Headers')
    print(json.dumps(dict(r.request.headers), indent=4))
    print('Response Body:')
    try:
        print(json.dumps(r.json(), indent=4, sort_keys=True))
    except json.JSONDecodeError:
        print(r.text)
    print()

def get (QUERY):
    r = requests.get(URL + QUERY)
    print_response(r)

def post (QUERY, DATA):
    r = requests.post(URL + QUERY, data=DATA)
    print_response(r)

def put (QUERY, DATA):
    r = requests.put(URL + QUERY, data=DATA)
    print_response(r)

def delete (QUERY):
    r = requests.delete(URL + QUERY)
    print_response(r)


if __name__ == '__main__':
    # get('api/article/v0/get_article_id/5712396000612')
    #post('api/placement/v1/update_by_article_id', {'article_id': '10', 'shelf': 'a-b-2'})
    # delete('api/instructions/v0/delete/bygg/varme_styring.pdf')
    post('api/cache/v0/set', {'mem_key': 'api_article_v0_min_stock_adjustment_id_for_2021_07_22', 'mem_val': '1080899'})
    #get('api/cache/v0/read/test')
    #delete('api/cache/v0/delete/min_momement_id_last_year')
