import json

from tests.test_data.elspot import load_elspot_test_data

FILES = {
    '23': 'tests/test_data/elspot/23/2023-03-26.json',
    '24': 'tests/test_data/elspot/24/2022-12-01.json',
    '25': 'tests/test_data/elspot/25/2022-10-30.json',
}

def elspot_test_data(self):
    json_23 = load_elspot_test_data(23)
    json_24 = load_elspot_test_data(24)
    json_25 = load_elspot_test_data(25)
