from cocuvida.environment import env_ini_get, env_var_get


def check_secret(secret: str) -> bool:
    if env_var_get('COCUVIDA_TESTING') == True:
        return True
    stored_secret = env_ini_get('cocuvida', 'secret')
    return (secret == stored_secret)
