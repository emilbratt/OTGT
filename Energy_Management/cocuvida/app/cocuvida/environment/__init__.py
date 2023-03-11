from os import getenv, path
import configparser


PATH_ENVIRONMENT_DOT_INI = '../../../environment.ini' # relative to workdir /OTGT/Energy_Management/cocuvida/app
# abs file-location in repo: /OTGT/environment.ini, checking if exists as first thing
if not path.isfile(PATH_ENVIRONMENT_DOT_INI):
    raise FileNotFoundError

# load values from envitonment.ini
def env_ini_get(section: str, key: str):
    config = configparser.ConfigParser()
    config.sections()
    config.read(PATH_ENVIRONMENT_DOT_INI)
    section = config[section]
    env = section[key].strip('"')
    return env

# load values from shell envars
def env_var_get(envar: str) -> str:
    env = getenv(envar)
    if env == None:
        print('Error: envar is not set')
        print(envar)
        raise KeyError
    return env
