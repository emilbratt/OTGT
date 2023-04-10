from .mqtt import mqtt_publish
from .exampletarget import exampletarget_publish
from .shelly import shelly_publish


class Target:
    def __init__(self, target_entry: dict):
        self.target_entry = target_entry
        print('target entry')
        print(target_entry)
        print()
        print()

    async def publish_state(self, target_type: str, state_value: str) -> bool:
        res = False
        match target_type:
            case 'exampletarget':
                res = await exampletarget_publish(self.target_entry, state_value)
            case 'mqtt':
                res = await mqtt_publish(self.target_entry, state_value)
            case 'shelly':
                res = await shelly_publish(self.target_entry, state_value)
            case _:
                raise Exception('UnknownEntryInTarget', target_type)

        return res
