from .QueryRetail import QueryRetail

class Retail:
    def __init__(self, config):
        print('this is Retail()')
        self.query = QueryRetail()
        print(config)

    def disconnect(self):
        self.cnxn = None

    def connect(self):
        # cnxn_string =
        try:
            self.cnxn = pyodbc.connect('DRIVER={FreeTDS};SERVER=%s;PORT=%s;DATABASE=%s;UID=%s;PWD=%s' % (
                                                    credentials['server'], credentials['port'],
                                                    credentials['database'], credentials['user'],
                                                    credentials['password']))
        except pyodbc.ProgrammingError:
            print(f'Getconnect: Could not connect to {credentials["database"]}')
            exit(1)
