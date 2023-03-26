from cocuvida.sqldatabase.controlplans import list_plan_names
from cocuvida.sqldatabase.controlplans import get_stringio_control_plan_by_name
from cocuvida.environment import env_ini_get

class View:

    HTML_START = b'''<!DOCTYPE html>
    <html>
    <head>
    '''

    HTML_HEAD_END = b'''
    </head>
    '''

    HTML_BODY_START = b'''
    <body>
    '''

    HTML_BODY_END = b'''
    </body>
    </html>
    '''

    OVERVIEW_URLS = [
        # [title, path]
        ['/controlplans', 'Controlplans'],
    ]

    def __init__(self):
        self.html_head = bytes()
        self.headers = {b'content-type': b'text/html'}
        self.html_title = b'<p>Cocuvida Home</p><hr>'
        self.html_overview = bytes()
        self.http_code = 200

    async def overview(self):
        rows = []
        for row in self.OVERVIEW_URLS:
            rows.append(f'<td><a href="{row[0]}">{row[1]}</a></td>'.encode())
        self.html_overview += b'''
        <p>Overview</p>
        <table>
        <tr>
        '''
        for row in rows:
            self.html_overview += row
        self.html_overview += b'''
        </tr>
        </table>
        <hr>
        '''

    async def send(self, send: object) -> None:
        headers = []
        for k,v in self.headers.items():
            headers.append([k,v])

        # SEND HTTP HEADER
        await send({
            'type': 'http.response.start',
            'status': self.http_code,
            'headers': headers,
        })

        # SEND HTTP BODY
        html_head_parts = [self.HTML_START + self.html_head + self.HTML_HEAD_END]
        for head in html_head_parts:
            await send({
                'type': 'http.response.body',
                'body': head,
                'more_body': True
            })
        await send({
            'type': 'http.response.body',
            'body': self.HTML_BODY_START,
            'more_body': True
        })
        html_body_parts = [self.html_title, self.html_overview]
        for body in html_body_parts:
            await send({
                'type': 'http.response.body',
                'body': body,
                'more_body': True
            })
        await send({
            'type': 'http.response.body',
            'body': self.HTML_BODY_END,
            'more_body': False
        })
        return None
