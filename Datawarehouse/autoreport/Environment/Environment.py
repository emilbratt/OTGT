from os import path
import configparser
ENVIRONMENT_FILE = '../../environment.ini'

if not path.isfile(ENVIRONMENT_FILE):
    exit('could not locate environment.ini stored in var ENVIRONMENT_FILE')

CONFIG = configparser.ConfigParser()
CONFIG.sections()
CONFIG.read(ENVIRONMENT_FILE)

def get(section, name):
    return CONFIG[section][name].strip('"')
