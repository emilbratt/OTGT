COLOURS = {
    'default': '\033[0m',
    'green': '\033[92m',
    'blue': '\033[94m',
    'red': '\033[31m',
    'brown': '\033[33m',
    'purple': '\033[95m',
    'aqua': '\033[96m',
    'yellow': '\033[93m',
}

FILES = {
    # this is the most "normal" case of elspot prices (nothing out of the ordinary here..)
    'normal': 'tests/test_data/elspot/normal/2022-12-01.json',

    # these files contains elsopt prices for non-24 hour days (for dailight savings time cases)
    '23': 'tests/test_data/elspot/23/2023-03-26.json',
    '25': 'tests/test_data/elspot/25/2022-10-30.json',

    # this file contains elspot prices that are below zero
    'negative': 'tests/test_data/elspot/negative/2023-04-10.json',
}
