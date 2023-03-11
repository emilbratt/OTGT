class View:

    TEMPLATE_START = '''
    <!DOCTYPE html>
    <html>
    <body>
    '''

    TEMPLATE_END = '''
    </body>
    </html>
    '''

    def __init__(self):
        self.template = ''
        self.http_code = 200

    def form_upload_control_plan(self):
        self.template += '''
        <form method="POST" enctype="multipart/form-data">
            <label for="controlplan">YAML:</label><br>
            <input type="file" id="controlplan" name="controlplan" accept=".yml,.yaml" required /><br>
            <label for="secret">Secret:</label><br>
            <input type="password" id="secret" name="secret" required /><br>
            <input type="submit" value="SUBMIT" /><br>
        </form>
        '''

    def un_authorized(self):
        self.http_code = 401
        self.template += '''
        <p>unauthorized</p>
        '''

    def invalid_yaml(self):
        self.http_code = 400
        self.template += '''
        <p>invalid yaml file</p>
        '''

    def db_action(self, action:str):
        self.http_code = 201
        match action:
            case 'insert':
                self.template += '''
                <p>Inserted new plan</p>
                '''
            case 'update':
                self.template += '''
                <p>Updated plan</p>
                '''
            case _:
                self.http_code = 500
                self.template += '''
                <p>Error</p>
                '''


    async def send(self, send: object):

        await send({
            'type': 'http.response.start',
            'status': self.http_code,
            'headers': [
                [b'content-type', b'text/html'],
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': self.TEMPLATE_START.encode(),
            'more_body': True
        })
        await send({
            'type': 'http.response.body',
            'body': self.template.encode(),
            'more_body': True
        })
        await send({
            'type': 'http.response.body',
            'body': self.TEMPLATE_END.encode(),
            'more_body': False
        })
