import unittest

from cocuvida.environment import env_ini_get

# options in environment.ini
ENVIRONMENT_OPTIONS = (
    'host',
    'port',
    'secret',
    'elspot_currency',
    'elspot_region',
    'elspot_plot_y_max',
    'elspot_plot_y_step',
)

VALID_CURRENCIES = ('NOK', 'EUR', 'SEK', 'DKK')

VALID_REGIONS = (
    'Bergen',
    'DK1',
    'DK2',
    'EE',
    'FI',
    'Kr.sand',
    'LT',
    'LV',
    'Molde',
    'Oslo',
    'SE1',
    'SE2',
    'SE3',
    'SE4',
    'SYS',
    'Tr.heim',
    'Tromsø',
)


def cocuvida(self: unittest.TestCase):
    # check if all options are present
    check = True
    missing = []
    for option in ENVIRONMENT_OPTIONS:
        if env_ini_get(section='cocuvida', key=option) == None:
            check = False
            missing.append(option)
    if check == False:
        print('ERROR: Mising environment.ini options')
        print('[cocuvida]')
        for m in missing:
            print(f'  {m}')
    self.assertTrue(check)

    # validate elspot_currency
    currency = env_ini_get(section='cocuvida', key='elspot_currency')
    self.assertTrue(currency in VALID_CURRENCIES)

    # validate elspot_region
    region = env_ini_get(section='cocuvida', key='elspot_region')
    self.assertTrue(region in VALID_REGIONS)
