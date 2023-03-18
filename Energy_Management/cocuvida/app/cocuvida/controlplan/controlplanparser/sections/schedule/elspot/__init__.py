from cocuvida.timehandle import isodates


class Entry:
    def __init__(self, elspot: dict):
        self.e = elspot

    async def generate_states(self, isodate: str):
        raise Exception('MethodNotImplemented')
