from cocuvida.sqldatabase.controlplans import list_plan_names
from cocuvida.sqldatabase.controlplans import get_stringio_control_plan_by_name


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
        self.html_head = bytes()
        self.headers = {b'content-type': b'text/html'}
        self.html_title = b'<p>Control Plans</p><hr>'
        self.html_invalid_yaml = bytes()
        self.html_forms = bytes()
        self.html_un_authorized = bytes()
        self.html_control_plan = bytes()
        self.file_control_plan = bytes()
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
        if len(plan_names) > 0:
            self.html_forms += b'''
            <p>Options</p>
            <form method="POST" action="" enctype="multipart/form-data">
            <select id="control_plan_options" name="plan_name">
            '''
            for name in plan_names:
                self.html_forms += f'<option value="{name}">{name}</option>'.encode()
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

    async def show_control_plan_data(self, plan_name: str):
        plan_data = await get_stringio_control_plan_by_name(plan_name)
        self.html_control_plan += b'<p>Control Plan</p><pre>' + plan_data + b'</pre><hr>'

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
        match action:
            case 'insert':
                self.http_code = 201
                msg = b'inserted control plan'
            case 'update':
                self.http_code = 201
                msg = b'updated control plan'
            case 'delete':
                self.http_code = 200
                msg = b'deleted control plan'
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
                               self.db_message, self.html_un_authorized, self.html_invalid_yaml,]
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
