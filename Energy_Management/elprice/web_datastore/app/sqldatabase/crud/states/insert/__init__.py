class Insert:
    def __init__(self, cnxn: object):
        self.cnxn = cnxn

    def bydate_v0(self, datamodel: object)-> str:
        action = None
        cursor = self.cnxn.cursor()
        the_region = datamodel.region
        the_date = datamodel.date
        the_json = datamodel.get_json_data()
        try:
            cursor.execute('''
                INSERT INTO states_by_date_v0
                    (the_region, the_date, the_json) 
                VALUES
                    (:the_region, :the_date, :the_json)
            ''', (the_region, the_date, the_json))
            self.cnxn.commit()
            action = 'inserted'
        except:
            cursor.execute('''
                SELECT the_json FROM states_by_date_v0
                WHERE the_region = :the_region AND the_date = :the_date
            ''', (the_region, the_date))
            res = cursor.fetchone()
            if res:
                current_json = res[0]
                if the_json == current_json:
                    action = 'validated'
                else:
                    cursor.execute('''
                        UPDATE states_by_date_v0
                        SET the_json = :the_json
                        WHERE the_region = :the_region AND the_date = :the_date
                    ''',
                    (the_json, the_region, the_date))
                    action = 'updated'
                    self.cnxn.commit()
        finally:
            self.cnxn.close()
            return action
