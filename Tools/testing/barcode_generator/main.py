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

def post (URL, data):
    r = requests.post(URL, json=data)
    print('POST request: ' + r.url)
    print('Response: ' + str(r.status_code))
    print(r.json())
    print()


if __name__ == '__main__':
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

    # test generating multiple shelf barcodes
    QUERY = 'shelf/'
    URL = HTTP + '://' + URL + ':' + PORT + '/' + QUERY
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
