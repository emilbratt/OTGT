from paho.mqtt import publish


class TargetMQTT:

    def __init__(self):
        self.entries = {}
        self.auth = {}
        self.host = None
        self.port = None
        self.client_id = None
        self.states = None
        self.tls = None
        self.keep_alive = None
        self.will = None
        self.transport = None

    async def load_target_entry(self, target_entry: dict) -> bool:
        try:
            self.auth['username'] = target_entry['username']
            self.auth['password'] = target_entry['password']
            self.host = target_entry['host']
            self.port = int(target_entry['port'])
            self.client_id = target_entry['client_id']
            self.states = target_entry['states']
            self.tls = target_entry['tls']
            self.keep_alive = int(target_entry['keep_alive'])
            self.will = target_entry['will']
            self.transport = target_entry['transport']
            for alias, entry in target_entry['entries'].items():
                self.entries[alias] = entry
        except KeyError:
            print(f'ERROR: target_entry mqtt is not valid')
            return False
        return True

    async def publish_state(self, alias: str, state: str) -> bool:
        try:
            topic = self.entries[alias]
        except KeyError:
            print(f'ERROR: controlplan mqtt->entries has no entry with {alias}')
            return False
        try:
            message = self.states[state]['message']
            retain = self.states[state]['retain']
            qos = int(self.states[state]['qos'])
        except KeyError:
            print(f'ERROR: controlplan mqtt->states has no entry with {state}')
            return False
        try:
            res = publish.single(
                topic=topic,
                payload=message,
                qos=qos,
                retain=retain,
                hostname=self.host,
                port=self.port,
                client_id=self.client_id,
                keepalive=self.keep_alive,
                will=self.will,
                auth=self.auth,
                tls=self.tls,
                transport=self.transport
            )
            return True
        except Exception as e:
            print(f'ERROR: mqtt publish failed with exception {e}')
            return False
