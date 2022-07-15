import os.path as path
import requests
import configparser

ENVIRONMENT_FILE = '../../../../environment.ini'
if not path.isfile(ENVIRONMENT_FILE):
    exit('could not locate environment.ini stored in var ENVIRONMENT_FILE')

config = configparser.ConfigParser()
config.sections()
config.read(ENVIRONMENT_FILE)
HOST = config['datawarehouse']['cip_info_host'].strip('"')
PORT = config['datawarehouse']['cip_info_port'].strip('"')
URL = 'http' + '://' + HOST + ':' + PORT + '/'
API_ENDPOINT_GET_ARTICLE_ID = 'api/article/v0/get_article_id/'
API_ENDPOINT_POST_PLACEMENT = 'api/placement/v1/update_by_article_id'


class Connect:

    def __init__(self):
        self.header = None
        self.body = None
        self.status_code = None

    def get_article_id (self, item):
        url = URL + API_ENDPOINT_GET_ARTICLE_ID + str(item)
        r = requests.get(url)
        self.status_code = r.status_code
        if self.status_code == 500: # invalid url to api
            print('Invalid API endpoint: ' + url)
            exit(1)
        self.header = dict(r.request.headers)
        self.body = dict(r.json())

    def post_placement (self, DATA):
        url = URL + API_ENDPOINT_POST_PLACEMENT
        r = requests.post(url, data=DATA)
        self.status_code = r.status_code
        if self.status_code == 500: # invalid url to api
            print('Invalid API endpoint: ' + url)
            exit(1)
        self.header = dict(r.request.headers)
        self.body = dict(r.json())
