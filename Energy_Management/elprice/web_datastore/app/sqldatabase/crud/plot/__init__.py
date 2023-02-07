class Operation:
    def __init__(self, cnxn: object):
        self.cnxn = cnxn

    def insert(self) -> object:
        from .insert import Insert
        return Insert(self.cnxn)

    def select(self) -> object:
        from .select import Select
        return Select(self.cnxn)
