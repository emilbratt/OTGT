import json
class Select:
    def __init__(self, cnxn: object):
        self.cnxn = cnxn

    def bydate_v0(self, the_region: str, the_date: str)-> object:
        cursor = self.cnxn.cursor()
        cursor.execute('''
            SELECT the_json FROM states_by_date_v0
            WHERE the_region = :the_region
            AND   the_date   = :the_date
        ''', (the_region, the_date))
        res = cursor.fetchone()
        self.cnxn.close()
        if res:
            return json.loads(res[0])
        else:
            return None
