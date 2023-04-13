import aiohttp
import asyncio


VALID_STATES = ['on', 'off', 'toggle']

async def get_valid_states() -> list:
    return VALID_STATES

async def shelly_publish(target_entry: dict, state_value: str, aiohttp_session: aiohttp.ClientSession) -> bool:
    if state_value not in VALID_STATES:
        raise Exception('InvalidState', state_value)

    http_user = target_entry['user']
    http_password = target_entry['password']
    http_auth = aiohttp.BasicAuth(http_user, http_password)

    tasks = []
    for alias, http_relay_path in target_entry['entries'].items():
        http_params = {'turn': state_value}
        async_coroutine = aiohttp_session.get(url=http_relay_path, params=http_params, auth=http_auth, ssl=False) 
        tasks.append(asyncio.create_task(async_coroutine))
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    publish_ok = True
    for r in responses:
        try:
            if r.status == 200:
                response = await r.json()
            else:
                response = await r.text()
                publish_ok = False
        except Exception as e:
            publish_ok = False

    return publish_ok
