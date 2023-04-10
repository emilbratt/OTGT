import aiohttp
import json


async def shelly_publish(target_entry: dict, state_value: str) -> bool:
    for alias, arr in target_entry.items():
        target_ip = arr[0]
        shelly_url = f'http://{target_ip}/rpc/Switch.Set'
        print('shelly publish to', target_ip, 'state', state_value)
        return True
        # target_id = arr[1]
        # match state_value:
        #     case 'on':
        #         payload = {'id': target_id, 'on': True}
        #     case 'off':
        #         payload = {'id': target_id, 'on': False}
        #     case _:
        #         raise Exception('UnsupportedState:', state_value)

        # # FIXME: make session operate for all entries in the target entry
        # async with aiohttp.ClientSession() as session:
        #     res = await session.post(shelly_url, json=payload)
        #     print(res)
