from cocuvida.timehandle import isodates


class Entry:
    def __init__(self, sun: dict):
        self.s = sun

    async def generate_states(self, isodate: str):
        raise Exception('MethodNotImplemented')
