import json

class Entry:
    def __init__(self, shelly: dict):
        self.target = shelly

    async def publish_state(self, state_value: str) -> bool:
        for alias, arr in self.target['entries'].items():
            shelly_url = f'http://{arr[0]}/rpc'
            payload = {'id': arr[1], state_value: True}
            payload = json.dumps(payload)
            print('alias:', alias, 'url:', shelly_url, 'payload', payload)
        return True