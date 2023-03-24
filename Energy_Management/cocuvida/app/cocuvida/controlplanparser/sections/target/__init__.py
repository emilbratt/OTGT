class Entry:
    def __init__(self, target_entry: dict):
        self.target_entry = target_entry

    async def publish_state(self, target_type: str, state_value: str) -> bool:
        match target_type:
            case 'exampletarget':
                from .exampletarget import Entry
            case 'mqtt':
                from .mqtt import Entry
            case 'shelly':
                from .shelly import Entry
            case _:
                raise Exception('UnknownEntryInTarget', target_type)

        obj = Entry(self.target_entry)
        res = await obj.publish_states(state_value)
        return res
