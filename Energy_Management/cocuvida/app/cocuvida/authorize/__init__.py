from cocuvida.environment import env_ini_get


def check_secret(secret: str) -> bool:
    stored_secret = env_ini_get('cocuvida', 'secret')
    return (secret == stored_secret)
