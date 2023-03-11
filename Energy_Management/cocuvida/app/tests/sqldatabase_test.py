from cocuvida.sqldatabase import scripts

def create_database(self):
    self.assertTrue(scripts.run('create_tables.sql'))
