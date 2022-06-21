from .QueryDatawarehouse import QueryDatawarehouse

class Datawarehouse:
    def __init__(self, config):
        print('this is Datawarehouse()')
        print(config)
        self.query = QueryDatawarehouse()
