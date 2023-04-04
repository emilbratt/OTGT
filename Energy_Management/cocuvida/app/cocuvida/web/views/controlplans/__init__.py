from cocuvida.sqldatabase.controlplans import get_stringio_control_plan_by_name
from cocuvida.sqldatabase.stateschedule import select_states_today_for_plan_name

from cocuvida.web.templates import forms, tables


class View:

    HTML_START = b'''<!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
    table, th, td {
        /* border: 1px solid white; */
        border: 1px solid black;
        border-collapse: collapse;
        text-align: center;
        /* color: green; */
    }
    /*
    body {background-color: black;}
    p    {color: green;}
    */
    </style>
    '''

    HTML_HEAD_END = b'''
    </head>
    '''

    HTML_BODY_START = b'''
    <body>
    <button onclick="window.location.href='/';">Home</button>
    '''

    HTML_BODY_END = b'''
    </body>
    </html>
    '''

    def __init__(self):
        self.html_head = bytes()
        self.headers = {b'content-type': b'text/html'}
        self.html_title = b'<p>Control Plans</p><hr>'
        self.html_invalid_yaml = bytes()
        self.html_forms = bytes()
        self.html_un_authorized = bytes()
        self.html_control_plan = bytes()
        self.html_state_schedule = bytes()
        self.file_control_plan = bytes()
        self.db_message = bytes()
        self.http_code = 200

    async def form_upload(self):
        self.html_forms += await forms.controlplan_upload()

    async def form_options(self):
        self.html_forms += await forms.controlplan_options()

    async def show_control_plan_data(self, plan_name: str):
        plan_data = await get_stringio_control_plan_by_name(plan_name)
        self.html_control_plan += b'<p>Control Plan</p><pre>' + plan_data + b'</pre><hr>'

    async def show_state_schedule(self, plan_name: str):
        res = await select_states_today_for_plan_name(plan_name)
        self.html_state_schedule += await tables.state_schedule(res)
        #self.html_state_schedule += b'<p>Control Plan</p><pre>' + plan_data + b'</pre><hr>'

    async def download_control_plan_data(self, plan_name: str):
        self.file_control_plan = await get_stringio_control_plan_by_name(plan_name)
        self.headers[b'content-type'] = b'application/x-yaml'

    async def un_authorized(self):
        self.http_code = 401
        self.html_un_authorized += b'<p>unauthorized</p>'

    async def invalid_yaml(self):
        self.http_code = 400
        self.html_invalid_yaml += b'<p>invalid yaml file</p>'

    async def db_action(self, action: str):
        msg = b'OK'
        match action:
            case 'insert':
                self.http_code = 201
            case 'update':
                self.http_code = 201
            case 'delete':
                self.http_code = 200
            case _:
                self.http_code = 500
                msg = action.encode()
        self.db_message += b'<p>' + msg + b'</p><hr>'

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
        if self.headers[b'content-type'] == b'application/x-yaml':
            await send({
                'type': 'http.response.body',
                'body': self.file_control_plan,
                'more_body': False
            })
            return None
        elif self.headers[b'content-type'] == b'text/html':
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
            html_body_parts = [self.html_title, self.html_forms, self.html_control_plan,
                               self.db_message, self.html_un_authorized, self.html_invalid_yaml,
                               self.html_state_schedule]
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
