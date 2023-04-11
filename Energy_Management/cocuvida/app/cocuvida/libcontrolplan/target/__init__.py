import aiohttp

from .mqtt import mqtt_publish
from .exampletarget import exampletarget_publish
from .shelly import shelly_publish


class Target:
    def __init__(self, target_entry: dict):
        self.target_entry = target_entry

    async def is_included(self, target_type: str) -> bool:
        is_included = self.target_entry[target_type]['include_entry']
        return is_included

    async def publish_state(self, target_type: str, state_value: str) -> bool:
        res = False
        match target_type:
            case 'exampletarget':
                res = await exampletarget_publish(self.target_entry['exampletarget'], state_value)
            case 'mqtt':
                res = await mqtt_publish(self.target_entry['mqtt'], state_value)
            case 'shelly':
                timeout = aiohttp.ClientTimeout(total=5)
                async with aiohttp.ClientSession(timeout=timeout) as aiohttp_session:
                    res = await shelly_publish(self.target_entry['shelly'], state_value, aiohttp_session)
            case _:
                raise Exception('UnknownTargetType', target_type)

        return res
