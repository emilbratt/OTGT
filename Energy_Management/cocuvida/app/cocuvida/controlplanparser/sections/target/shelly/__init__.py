class Entry:
    def __init__(self, shelly: dict):
        self.target = shelly

    async def publish_states(self, state_value: str) -> bool:
        for entry in self.target['entries']:
            msg = ('key:', entry, 'Value:', self.target['entries'][entry])
        return True