class View:

    FAVICON_ICO = 'cocuvida/web/views/favicon/favicon.ico'

    def __init__(self):
        with open(self.FAVICON_ICO, 'rb', buffering=0) as f:
            self.favicon = f.read()

    async def send(self, send: object) -> None:
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'image/x-icon'],
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': self.favicon,
        })
        return None
