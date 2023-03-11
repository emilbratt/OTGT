class View:

    TEMPLATE_START = '''
    <!DOCTYPE html>
    <html>
    <body>
      <form method="POST" enctype="multipart/form-data">
      <div>
        <label for="controlplan">YAML:</label><br>
        <input type="file" id="controlplan" name="controlplan" accept=".yml,.yaml" required />
      </div>

      <div>
        <label for="pwd">Secret:</label><br>
        <input type="password" id="secret" name="secret" required />
      </div>

      <div>
        <input type="submit" value="SUBMIT" />
      </div>
    </form>
    '''

    TEMPLATE_END = '''
    </body>
    </html>
    '''

    def __init__(self):
        self.template = ''
        self.http_code = 200

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
