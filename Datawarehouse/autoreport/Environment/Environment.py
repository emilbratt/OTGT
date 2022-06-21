from os import path
import configparser
ENVIRONMENT_FILE = '../../environment.ini'

if not path.isfile(ENVIRONMENT_FILE):
    exit('could not locate environment.ini stored in var ENVIRONMENT_FILE')

CONFIG = configparser.ConfigParser()
CONFIG.sections()
CONFIG.read(ENVIRONMENT_FILE)

def database_retail():
    conf = {}
    conf['host'] = CONFIG['retail']['db_host'].strip('"')
    conf['port'] = CONFIG['retail']['db_port'].strip('"')
    conf['db'] = CONFIG['retail']['db_name'].strip('"')
    conf['user'] = CONFIG['retail']['db_user'].strip('"')
    conf['password'] = CONFIG['retail']['db_password'].strip('"')
    return conf

def database_datawarehouse():
    conf = {}
    conf['host'] = CONFIG['datawarehouse']['db_host'].strip('"')
    conf['port'] = CONFIG['datawarehouse']['db_port'].strip('"')
    conf['db'] = CONFIG['datawarehouse']['db_name'].strip('"')
    conf['user'] = CONFIG['datawarehouse']['db_user_post'].strip('"')
    conf['password'] = CONFIG['datawarehouse']['db_password_post'].strip('"')
    return conf
