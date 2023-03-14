from cocuvida.environment import env_ini_get


CURRENCY_CONFIG = {
    'NOK': {'currency': 'NOK', 'original_price_unit': 'NOK/MWh', 'reshape_price_unit': 'ore/kWh'},
    'EUR': {'currency': 'EUR', 'original_price_unit': 'EUR/MWh', 'reshape_price_unit': 'EUR/MWh'},
}

def get():
    try:
        country_code = env_ini_get('cocuvida', 'elspot_currency')
        return CURRENCY_CONFIG[country_code]
    except KeyError:
        return False

def msg_valid_keys():
    msg = 'Use one of the keys below\n'
    for key in CURRENCY_CONFIG:
        msg += key + '\n'
    return msg
