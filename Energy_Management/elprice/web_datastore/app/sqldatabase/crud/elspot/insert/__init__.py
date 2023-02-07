class Insert:
    def __init__(self, cnxn: object):
        self.cnxn = cnxn

    def raw_v0(self, datamodel: object)-> str:
        action = None
        cursor = self.cnxn.cursor()
        the_date = datamodel.get_date()
        the_json = datamodel.get_json_data()
        try:
            cursor.execute('''
                INSERT INTO elspot_raw_v0
                    (the_date, the_json) 
                VALUES
                    (:the_date, :the_json)
            ''', (the_date, the_json))
            self.cnxn.commit()
            action = 'inserted'
        except:
            query = ('''
                SELECT the_json
                FROM elspot_raw_v0
                WHERE the_date = '%s'
            ''' %the_date)
            cursor.execute(query)
            res = cursor.fetchone()
            if res:
                current_json = res[0]
                if the_json == current_json:
                    action = 'validated'
                else:
                    cursor.execute('''
                        UPDATE elspot_raw_v0
                        SET the_json = :the_json
                        WHERE the_date = :the_date
                    ''',
                    (the_json, the_date))
                    action = 'updated'
                    self.cnxn.commit()
        finally:
            self.cnxn.close()
            return action

    def reshaped_v0(self, datamodel: object)-> str:
        action = None
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
            action = 'inserted'
        except:
            cursor.execute('''
                SELECT the_region, the_date, the_json FROM elspot_reshaped_v1
                WHERE the_region = :the_region AND the_date = :the_date
            ''', (the_region, the_date))
            res = cursor.fetchone()
            if res:
                current_json = res[2]
                if the_json == current_json:
                    action = 'validated'
                else:
                    cursor.execute('''
                        UPDATE elspot_reshaped_v1
                        SET the_json = :the_json
                        WHERE the_region = :the_region AND the_date = :the_date
                    ''',
                    (the_json, the_region, the_date))
                    action = 'updated'
                    self.cnxn.commit()
        finally:
            self.cnxn.close()
            return action

    def reshaped_v1(self, datamodel: object)-> str:
        action = None
        cursor = self.cnxn.cursor()
        the_date = datamodel.get_date()
        the_json = datamodel.get_json_data()
        try:
            cursor.execute('''
                INSERT INTO elspot_reshaped_v1
                    (the_date, the_json) 
                VALUES
                    (:the_date, :the_json)
            ''', (the_date, the_json))
            self.cnxn.commit()
            action = 'inserted'
        except:
            cursor.execute('''
                SELECT the_json FROM elspot_reshaped_v1
                WHERE the_date = '%s'
            ''' %the_date)
            res = cursor.fetchone()
            if res:
                current_json = res[0]
                if the_json == current_json:
                    action = 'validated'
                else:
                    cursor.execute('''
                        UPDATE elspot_reshaped_v1
                        SET the_json = :the_json
                        WHERE the_date = :the_date
                    ''',
                    (the_json, the_date))
                    action = 'updated'
                    self.cnxn.commit()
        finally:
            self.cnxn.close()
            return action
