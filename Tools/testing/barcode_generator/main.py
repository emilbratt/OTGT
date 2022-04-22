#!/usr/bin/env python3

import sys
import requests
import configparser
import os
import json

# declare global variables
ENVIRONMENT_FILE = '../../../environment.ini'
URL = False # base url to api which is loaded from environment.ini
PORT = False # for testing against developement environment
QUERY = False # value after url, for example: api/test/v01/hello
HTTP = False # contains either http or https
USE_TLS = False # will swap http with https

def get_url (query):
    if not os.path.isfile(ENVIRONMENT_FILE):
        exit('could not locate environment.ini stored in var ENVIRONMENT_FILE')
    config = configparser.ConfigParser()
    config.sections()
    config.read(ENVIRONMENT_FILE)
    URL = config['datawarehouse']['datawarehouse_ip'].strip('"')
    PORT = config['datawarehouse']['barcode_generator_port'].strip('"')
    HTTP = 'http'
    if USE_TLS:
        HTTP = 'https'
    return HTTP + '://' + URL + ':' + PORT + '/' + query

def post (URL, data):
    r = requests.post(URL, json=data)
    print('POST request: ' + r.url)
    print('Response: ' + str(r.status_code))
    print(r.headers['content-type'])
    print('Response Headers')
    print(json.dumps(dict(r.request.headers), indent = 4))
    if r.headers['content-type'] ==  'application/json':
        print(json.dumps(r.json(), indent=4, sort_keys=True))

def get (URL):
    r = requests.get(URL)
    print('GET request: ' + r.url)
    print('Response: ' + str(r.status_code))
    print(r.headers['content-type'])
    print('Response Headers')
    print(json.dumps(dict(r.request.headers), indent = 4))
    if r.headers['content-type'] ==  'application/json':
        print(json.dumps(r.json(), indent=4, sort_keys=True))


if __name__ == '__main__':

    URL = get_url('test/post')
    post(URL, {"caller": "python test script"})

    URL = get_url('test/get')
    get(URL)

    URL = get_url('shelf/')
    data = {
        "barcodes":
            [
                "A-A-1", "A-A-2", "A-A-3", "A-A-4", "A-A-5", "A-A-6",
                "A-A-7", "A-A-8", "A-A-9", "A-A-10", "A-A-11", "A-A-12",
                "A-A-13", "A-A-14", "A-A-15", "A-A-16", "A-A-17", "A-A-18",
                "A-A-19", "A-A-20", "A-A-21", "A-A-22", "A-A-23", "A-A-24",
                "A-A-25", "A-A-26", "A-A-27", "A-A-28", "A-A-29", "A-A-30",
                "A-A-31", "A-A-32", "A-A-33", "A-A-34", "A-A-35", "A-A-36",
            ],
        "caller": "python test script"
    }
    post(URL, data)
