from yaml import safe_load as yaml_safe_load

from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import ValueTarget, FileTarget, NullTarget, SHA256Target
# package https://pypi.org/project/streaming-form-data/
# docs https://streaming-form-data.readthedocs.io/en/latest/#


class FormDataParser:

    def __init__(self, scope: dict, receive: object):
        self.receive = receive
        self.has_formdata = False

        # body is set to None because init function is not awaitable
        self.body = None

        # load headers into python dict (for compatibility with streaming-form-data)
        self.headers = {}
        for header in scope['headers']:
            key = header[0].decode()
            val = header[1].decode()
            if 'multipart/form-data' in val:
                self.has_formdata = True
            self.headers[key] = val

        if not self.has_formdata:
            print('ERROR: NO FORM DATA FOUND')


    # we load the body one time during first call to one of the async methods
    async def _load_body(self):
        # load request body into byte string
        self.body = b''
        more_body = True
        while more_body:
            message = await self.receive()
            self.body += message.get('body', b'')
            more_body = message.get('more_body', False)

    async def load_string(self, name: str):
        if not self.has_formdata:
            return None
        if self.body == None:
            await self._load_body()
        parser = StreamingFormDataParser(headers=self.headers)
        value = ValueTarget()
        parser.register(name, value)
        parser.data_received(self.body)
        data = value.value.decode('utf-8')
        if data == '':
            print('ERROR: NO FORM DATA FOR', name)
            return None
        return data

    async def load_yaml(self, name: str):
        if not self.has_formdata:
            return None
        if self.body == None:
            await self._load_body()
        parser = StreamingFormDataParser(headers=self.headers)
        value = ValueTarget()
        parser.register(name, value)
        parser.data_received(self.body)
        data = value.value.decode('utf-8')
        if data == '':
            return None
        try:
            data = yaml_safe_load(data)
            return data
        except:
            print('ERROR: INVALID YAML PASSED')
            return None

    # this method is not in used as of now
    async def write(self, name: str, filename: str):
        if not self.has_formdata:
            return None
        if self.body == None:
            await self._load_body()
        parser = StreamingFormDataParser(headers=headers)
        parser.register(name, FileTarget('/tmp/' + filename))
        parser.data_received(self.body)

    # this method is not in used as of now
    async def sha256(self, name: str):
        if not self.has_formdata:
            return None
        if self.body == None:
            await self._load_body()
        parser = StreamingFormDataParser(headers=self.headers)
        value = SHA256Target()
        parser.register(name, value)
        parser.data_received(self.body)
        checksum = value.value
        return checksum
