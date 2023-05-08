import aiohttp

from . import exampletarget, mqtt, shelly


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
                res = await exampletarget.publish(self.target_entry['exampletarget'], state_value)
            case 'mqtt':
                res = await mqtt.publish(self.target_entry['mqtt'], state_value)
            case 'shelly':
                res = await shelly.publish(self.target_entry['shelly'], state_value)
            case _:
                raise Exception('UnknownTargetType', target_type)

        return res
