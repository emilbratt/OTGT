from cocuvida.sqldatabase.controlplans import list_plan_names
import json

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

    def __init__(self):
        self.headers = {b'content-type': b'text/html'}
        self.html_head = bytes()
        self.html_body = b'<p>Control Plans</p><hr>'
        self.html_forms = bytes()
        self.yaml_body = bytes()
        self.db_message = bytes()
        self.http_code = 200

    async def form_upload(self):
        self.html_forms += b'''
        <p>Upload</p>
        <form method="POST" action="" enctype="multipart/form-data">
            <input type="file" id="upload_control_plan"
                   name="control_plan" accept=".yml,.yaml" required /><br>
            <label for="secret">Secret:</label>
            <input type="password" id="secret" name="secret" required />
            <button type="submit" name="submit" value="upload">Upload</button>
        </form>
        <hr>
        '''

    async def form_options(self):
        plan_names = await list_plan_names()
        if not plan_names:
            return None
        self.html_forms += b'''
        <p>Options</p>
        <form method="POST" action="" enctype="multipart/form-data">
        <select id="control_plan_options" name="plan_name">
        '''
        for plan_name in plan_names:
            self.html_forms += f'<option value="{plan_name[0]}">{plan_name[0]}</option>'.encode()
        self.html_forms += b'''
        </select><br>
        <label for="secret">Secret:</label>
        <input type="password" id="secret" name="secret" required />
        <button type="submit" name="submit" value="show">
            Show
        </button>
        <button type="submit" name="submit" value="download">
            Download
        </button>
        <button type="submit" name="submit" onclick="return confirm('Confirm deletion');" value="delete">
            Delete
        </button>
        </form>
        <hr>
        '''

    async def show_control_plan_data(self, plan_data: bytes):
        self.yaml_body += b'<pre>' + plan_data + b'</pre><hr>'

    async def download_control_plan_data(self, plan_data: bytes):
        self.yaml_body = plan_data
        self.headers[b'content-type'] = b'application/x-yaml'

    async def un_authorized(self):
        self.http_code = 401
        self.html_body += b'<p>unauthorized</p>'

    async def invalid_yaml(self):
        self.http_code = 400
        self.html_body += b'<p>invalid yaml file</p>'

    async def db_action(self, action: str):
        match action:
            case 'insert':
                self.http_code = 201
                self.db_message += b'<p>Inserted control plan</p><hr>'
            case 'update':
                self.http_code = 201
                self.db_message += b'<p>Updated control plan</p><hr>'
            case 'delete':
                self.http_code = 200
                self.db_message += b'<p>Deleted control plan</p><hr>'

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
                'body': self.yaml_body,
                'more_body': False
            })
            return None
        elif self.headers[b'content-type'] == b'text/html':
            html_head = self.HTML_START + self.html_head + self.HTML_HEAD_END
            html_body = self.html_body + self.html_forms + self.yaml_body + self.db_message
            await send({
                'type': 'http.response.body',
                'body': html_head,
                'more_body': True
            })
            await send({
                'type': 'http.response.body',
                'body': self.HTML_BODY_START,
                'more_body': True
            })
            await send({
                'type': 'http.response.body',
                'body': html_body,
                'more_body': True
            })
            await send({
                'type': 'http.response.body',
                'body': self.HTML_BODY_END,
                'more_body': False
            })
            return None
