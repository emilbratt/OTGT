#!/usr/bin/env python3

# a very simple test script
#
# some actions are triggered when data is received
# and this script can also help trigger these actions

import sys
import requests
import configparser
from os import path
import json

URL_WEB_DATASTORE = 'http://localhost:8085'
DIR_TEST_DATA = './test_data'
ELSPOT_RAW = path.join(DIR_TEST_DATA, 'elspot', 'raw_2023-01-23.json')
ELSPOT_RESHAPED = path.join(DIR_TEST_DATA, 'elspot', 'reshaped_2023-01-23.json')
PLOT_BYDATE_OSLO = path.join(DIR_TEST_DATA, 'plot', 'bydate_Oslo_2023-01-23.svg')
PLOT_BYHOUR_OSLO = path.join(DIR_TEST_DATA, 'plot', 'byhour_Oslo_2023-01-23_3.svg')

def print_response(r: object, r_type: str):
    print('HTTP REQUEST')
    print('TYPE:', r_type)
    print('URL:', r.url)
    print('RESPONSE CODE:', str(r.status_code))
    print('CONTENT-TYPE', r.headers['content-type'])
    print('RESPONSE HEADER')
    print(json.dumps(dict(r.request.headers), indent = 4, sort_keys=True))
    match r_type:
        case 'HEAD':
            return True
        case 'POST':
            pass
        case 'GET':
            pass

    print('RESPONSE BODY')
    if r.headers['content-type'] == 'application/json':
        print(json.dumps(r.json(), indent=4, sort_keys=True))
    else:
        print(r.text)

def POST(URL, data):
    r = requests.post(URL, json=data)
    print_response(r, 'POST')

def GET(URL):
    r = requests.get(URL)
    print_response(r, 'GET')

def HEAD(URL):
    r = requests.head(URL)
    print_response(r, 'HEAD')


def main(test: int):

    '''
        pass a number when calling this script,
        whatever the number, the match/case block will run
    '''

    url = URL_WEB_DATASTORE
    if len(sys.argv) == 1:
        test = 1
    else:
        test = int(sys.argv[1])

    match test:
        case 1:
            url = URL_WEB_DATASTORE + '/elspot/raw/v0'
            with open(ELSPOT_RAW) as my_file:
                data = json.load(my_file)
                postdata = {}
                postdata['data'] = data
                postdata['date'] = data['endDate']
                POST(url, postdata)
        case 2:
            url = URL_WEB_DATASTORE + '/elspot/reshaped/v1'
            with open(ELSPOT_RESHAPED, 'r') as my_file:
                data = json.load(my_file)
                postdata = {}
                postdata['date'] = data[0]['date']
                postdata['data'] = data
                POST(url, postdata)
        case 3:
            url = URL_WEB_DATASTORE + '/elspot/raw/v0'
            print('checking date 2023-01-23')
            HEAD(url + '/2023-01-23')
            print('checking date 1999-01-23')
            HEAD(url + '/1999-01-23')
        case 4:
            url = URL_WEB_DATASTORE + '/plot/bydate/v0'
            with open(PLOT_BYDATE_OSLO, 'r') as my_file:
                my_file = open(PLOT_BYDATE_OSLO, 'r', encoding='utf-8')
                svg_text = my_file.read()
                postdata = {}
                postdata['date'] = '2023-01-23'
                postdata['region'] = 'Oslo'
                postdata['data'] = svg_text
                POST(url, postdata)
        case 5:
            url = URL_WEB_DATASTORE + '/plot/byhour/v0'
            with open(PLOT_BYDATE_OSLO, 'r') as my_file:
                my_file = open(PLOT_BYHOUR_OSLO, 'r', encoding='utf-8')
                svg_text = my_file.read()
                postdata = {}
                postdata['date'] = '2023-01-23'
                postdata['region'] = 'Oslo'
                postdata['index'] = 3
                postdata['hour'] = 3
                postdata['data'] = svg_text
                POST(url, postdata)

main(test=5)
