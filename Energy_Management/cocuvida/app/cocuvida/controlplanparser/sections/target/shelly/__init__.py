import aiohttp
import json


class Entry:
    def __init__(self, shelly: dict):
        self.target = shelly

    async def publish_state(self, state_value: str) -> bool:
        for alias, arr in self.target['entries'].items():
            target_ip = arr[0]
            shelly_url = f'http://{target_ip}/rpc/Switch.Set'

            target_id = arr[1]
            match state_value:
                case 'on':
                    payload = {'id': target_id, 'on': True}
                case 'off':
                    payload = {'id': target_id, 'on': False}
                case _:
                    raise Exception('UnsupportedState:', state_value)

            print('PUIBLISH STATE')
            print('alias:', alias, 'url:', shelly_url, 'payload', payload)
            async with aiohttp.ClientSession() as session:
                res = await session.post(shelly_url, json=payload)
                print(res)
