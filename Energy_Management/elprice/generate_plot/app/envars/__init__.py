from os import getenv

def envar_get(ENVAR: str) -> str:
    env = getenv(ENVAR)
    if env == None:
        print(__file__)
        print('Error: envar is not set')
        print(ENVAR)
        exit(1)
    return env
