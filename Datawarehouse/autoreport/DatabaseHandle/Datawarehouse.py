from .QueryDatawarehouse import QueryDatawarehouse

class Datawarehouse:
    def __init__(self):
        print('this is Datawarehouse()')
        self.query = QueryDatawarehouse()
