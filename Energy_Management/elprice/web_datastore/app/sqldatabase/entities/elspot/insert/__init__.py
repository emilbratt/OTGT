import json
class Insert:
    def __init__(self, cnxn: object):
        self.cnxn = cnxn
        self.action = None

    def reshaped_v1(self, datamodel: object)-> str:
        cursor = self.cnxn.cursor()
        the_region = datamodel.get_region()
        the_date = datamodel.get_date()
        the_json = datamodel.get_json_data()
        try:
            cursor.execute('''
                INSERT INTO elspot_reshaped_v1
                    (the_region, the_date, the_json) 
                VALUES
                    (:the_region, :the_date, :the_json)
            ''', (the_region, the_date, the_json))
            self.cnxn.commit()
            self.action = 'inserted'
        except:
            cursor.execute('''
                SELECT the_region, the_date, the_json FROM elspot_reshaped_v1
                WHERE the_region = :the_region AND the_date = :the_date
            ''', (the_region, the_date))
            res = cursor.fetchone()
            if res:
                current_json = res[2]
                if the_json == current_json:
                    self.action = 'validated'
                else:
                    try:
                        cursor.execute('''
                            UPDATE elspot_reshaped_v1
                            SET the_json = :the_json
                            WHERE the_region = :the_region AND the_date = :the_date
                        ''',
                        (the_json, the_region, the_date))
                        self.action = 'updated'
                        self.cnxn.commit()
                    except:
                        self.action = 'failed'
        finally:
            self.cnxn.close()
            return self.action


    def raw_v1(self, datamodel: object)-> str:
        cursor = self.cnxn.cursor()
        the_date = datamodel.get_date()
        the_json = datamodel.get_json_data()
        try:
            cursor.execute('''
                INSERT INTO elspot_raw_v1
                    (the_date, the_json) 
                VALUES
                    (:the_date, :the_json)
            ''', (the_date, the_json))
            self.cnxn.commit()
            self.action = 'inserted'
        except:
            query = ('''
                SELECT the_date, the_json
                FROM elspot_raw_v1
                WHERE the_date = '%s'
            ''' %the_date)
            cursor.execute(query)
            res = cursor.fetchone()
            if res:
                current_json = res[1]
                if the_json == current_json:
                    self.action = 'validated'
                else:
                    try:
                        cursor.execute('''
                            UPDATE elspot_raw_v1
                            SET the_json = :the_json
                            WHERE the_date = :the_date
                        ''',
                        (the_json, the_date))
                        self.action = 'updated'
                        self.cnxn.commit()
                    except:
                        self.action = 'failed'
        finally:
            self.cnxn.close()
            return self.action
