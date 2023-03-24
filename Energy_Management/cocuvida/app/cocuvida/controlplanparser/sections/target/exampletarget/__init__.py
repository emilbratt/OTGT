class Entry:
    def __init__(self, exampletarget: dict):
        self.target = exampletarget

    async def publish_states(self, state_value: str) -> bool:
        '''
            this is just an example target, we always return publish = True
        '''
        for entry in self.target['entries']:
            msg = ('key:', entry, 'Value:', self.target['entries'][entry])
        return True