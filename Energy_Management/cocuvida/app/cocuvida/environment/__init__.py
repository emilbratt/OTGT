import configparser
import os


PATH_ENVIRONMENT_DOT_INI = '../../../environment.ini' # relative to workdir /OTGT/Energy_Management/cocuvida/app
# abs file-location in repo: /OTGT/environment.ini, checking if exists as first thing
if not os.path.isfile(PATH_ENVIRONMENT_DOT_INI):
    raise FileNotFoundError

ENV_INI = configparser.ConfigParser()
ENV_INI.sections()
ENV_INI.read(PATH_ENVIRONMENT_DOT_INI)

# load values from envitonment.ini
def env_ini_get(section: str, key: str):
    try:
        section = ENV_INI[section]
        env = section[key].strip('"')
        return env
    except KeyError:
        return None

# load values from shell envars
def env_var_get(envar: str) -> str:
    env = os.getenv(envar)
    match env:
        case 'false'|'False':
            return False
        case 'true'|'True':
            return True
        case None:
            print(f'WARNING: envar {envar} is not set')
            return None
        case _:
            return env
