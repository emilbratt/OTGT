#!/usr/bin/env python3

import sys
import requests
import configparser
import json
from os import path

from elspotmetadata  import levels, shapes
from elspotgenerate  import Generate
import elspotvisualize

URL_WEB_DATASTORE = 'http://localhost:8085'
DIR_TEST_DATA = './test_data'
ELSPOT_RAW = path.join(DIR_TEST_DATA, 'elspot', 'raw_2023-01-23.json')
ELSPOT_RESHAPED = path.join(DIR_TEST_DATA, 'elspot', 'reshaped_2023-02-21.json')
PLOT_BYDATE_OSLO = path.join(DIR_TEST_DATA, 'plot', 'bydate_Oslo_2023-01-23.svg')
PLOT_BYHOUR_OSLO = path.join(DIR_TEST_DATA, 'plot', 'byhour_Oslo_2023-01-23_3.svg')
STATES_BYDATE_OSLO = path.join(DIR_TEST_DATA, 'states', 'bydate_Oslo_2023-01-23.json')


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


def main():

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
                svg_text = my_file.read()
                postdata = {}
                postdata['date'] = '2023-01-23'
                postdata['region'] = 'Oslo'
                postdata['data'] = svg_text
                POST(url, postdata)
        case 5:
            url = URL_WEB_DATASTORE + '/plot/byhour/v0'
            with open(PLOT_BYHOUR_OSLO, 'r') as my_file:
                svg_text = my_file.read()
                postdata = {}
                postdata['date'] = '2023-01-23'
                postdata['region'] = 'Oslo'
                postdata['index'] = 3
                postdata['hour'] = 3
                postdata['data'] = svg_text
                POST(url, postdata)
        case 6:
            url = URL_WEB_DATASTORE + '/states/bydate/v0'
            with open(STATES_BYDATE_OSLO, 'r') as my_file:
                the_json = json.load(my_file)
                postdata = {}
                postdata['date'] = '2023-01-23'
                postdata['region'] = 'Oslo'
                postdata['data'] = the_json
                POST(url, postdata)
        case 7:
            gnrt = Generate()
            gnrt.from_val(10)
            gnrt.to_val(1000)
            gnrt.fluctuate_level(6)
            gnrt.spike_level(0)
            gnrt.dip_level(0)
            gnrt.set_date('2000-01-01')
            gnrt.set_region('Oslo')
            gnrt.split_hours(4)
            gnrt.sort_prices()
            gnrt.sort_offset_factor(5)
            gnrt.initialize()
            data = gnrt.generate_prices()
            elspotvisualize.reshaped_overview(data)
            elspotvisualize.reshaped_horizontal_curve(data)

        case 8:
            with open(ELSPOT_RESHAPED, 'r') as my_file:
                data = json.load(my_file)
                trondheim = data[12]
                bergen = data[10]
                oslo = data[8]

                print('Trondheim')
                elspotvisualize.reshaped_horizontal_curve(trondheim)
                price_list = [x['value'] for x in trondheim['prices']]
                slope = shapes.slope(price_list)
                print('slope', slope)
                elspotvisualize.percent_bar(slope,0,10)
                spike = shapes.spike(price_list)
                print('spike', spike)
                elspotvisualize.percent_bar(spike,-100,100)
                print()

                print('Bergen')
                elspotvisualize.reshaped_horizontal_curve(bergen)
                price_list = [x['value'] for x in bergen['prices']]
                slope = shapes.slope(price_list)
                print('slope', slope)
                elspotvisualize.percent_bar(slope,0,10)
                spike = shapes.spike(price_list)
                print('spike', spike)
                elspotvisualize.percent_bar(spike,-100,100)
                print()

        case 9:
            gnrt = Generate()
            gnrt.split_hours(4)
            gnrt.from_val(100)
            gnrt.to_val(130)
            gnrt.fluctuate_level(10)
            gnrt.spike_level(0)
            gnrt.dip_level(10)
            gnrt.initialize()
            data = gnrt.generate_prices()
            elspotvisualize.reshaped_overview(data)
            price_list = gnrt.get_price_list()
            elspotvisualize.horizontal_curve(price_list)

            slope = shapes.slope(price_list)
            print('slope', slope)
            elspotvisualize.percent_bar(slope,0,10)

            spike = shapes.spike(price_list)
            print('spike', spike)
            elspotvisualize.percent_bar(spike,-100,100)
            percent_of_max = levels.percent_of_max(price_list)
            diff_factor_range = levels.diff_factor_range(price_list)
            weight_range = levels.weight_range(price_list)

main()
