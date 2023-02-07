import json
class Select:
    def __init__(self, cnxn: object):
        self.cnxn = cnxn

    def raw_v0(self, the_date: str)-> object:
        cursor = self.cnxn.cursor()
        cursor.execute('''
            SELECT the_json FROM elspot_raw_v0
            WHERE the_date = :the_date
            ''', [the_date])
        res = cursor.fetchone()
        self.cnxn.close()
        if res:
            return json.loads(res[0])
        else:
            return None

    def raw_exists_v0(self, the_date: str)-> bool:
        cursor = self.cnxn.cursor()
        cursor.execute('''
            SELECT COUNT(the_json) FROM elspot_raw_v0
            WHERE the_date = :the_date
            ''', [the_date])
        res = cursor.fetchone()[0]
        return (res > 0)

    def reshaped_v0(self, the_region: str, the_date: str)-> object:
        cursor = self.cnxn.cursor()
        cursor.execute('''
            SELECT the_json FROM elspot_reshaped_v0
            WHERE the_region = :the_region
            AND   the_date   = :the_date
        ''', (the_region, the_date))
        res = cursor.fetchone()
        self.cnxn.close()
        if res:
            return json.loads(res[0])
        else:
            return None

    def reshaped_all_v0(self, the_date: str)-> object:
        cursor = self.cnxn.cursor()
        cursor.execute('''
            SELECT the_json FROM elspot_reshaped_v0
            WHERE the_date = :the_date
        ''', [the_date])
        res = cursor.fetchone()
        self.cnxn.close()
        if res:
            return json.loads(res[0])
        else:
            return None

    def reshaped_exists_v0(self, the_region: str, the_date: str) -> bool:
        cursor = self.cnxn.cursor()
        cursor.execute('''
            SELECT COUNT(the_json) FROM elspot_reshaped_v0
            WHERE the_region = :the_region
            AND   the_date   = :the_date
        ''', (the_region, the_date))
        res = cursor.fetchone()[0]
        return (res > 0)

    def reshaped_v1(self, the_date: str)-> object:
        cursor = self.cnxn.cursor()
        cursor.execute('''
            SELECT the_json FROM elspot_reshaped_v1
            WHERE the_date = :the_date
        ''', [the_date])
        res = cursor.fetchone()
        self.cnxn.close()
        if res:
            return json.loads(res[0])
        else:
            return None

    def reshaped_exists_v1(self, the_date: str) -> bool:
        cursor = self.cnxn.cursor()
        cursor.execute('''
            SELECT COUNT(the_json) FROM elspot_reshaped_v1
            WHERE the_date = :the_date
        ''', [the_date])
        res = cursor.fetchone()[0]
        return (res > 0)
