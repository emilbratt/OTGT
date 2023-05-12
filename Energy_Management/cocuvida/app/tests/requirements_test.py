import importlib
import unittest

REQUIREMENTS = (
    'aiofiles',
    'aiohttp',
    'paho',
    'streaming_form_data',
    'uvicorn',
    'uvloop',
    'yaml',
    'matplotlib',
    'numpy',
)


def check_modules(self: unittest.TestCase):
    check = True
    missing = []
    for requirement in REQUIREMENTS:
        if importlib.util.find_spec(requirement) == None:
            check = False
            missing.append(requirement)
    if check == False:
        print('ERROR: Mising modules')
        for m in missing:
            print(f' - {m}')
    self.assertTrue(check)
