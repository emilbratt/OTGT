from os import getenv

def envar_get(NAME: str) -> str:
    env = getenv(NAME)
    if env == None:
        print(__file__)
        print('Error: envar is not set')
        print(NAME)
        exit(1)
    return env
