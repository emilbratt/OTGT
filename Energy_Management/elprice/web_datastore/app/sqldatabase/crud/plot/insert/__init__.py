class Insert:
    def __init__(self, cnxn: object):
        self.cnxn = cnxn

    def bydate_v0(self, datamodel: object)-> str:
        action = None
        cursor = self.cnxn.cursor()
        the_region = datamodel.region
        the_date = datamodel.date
        the_svg = datamodel.data
        try:
            cursor.execute('''
                INSERT INTO plot_by_date_v0
                    (the_region, the_date, the_svg) 
                VALUES
                    (:the_region, :the_date, :the_svg)
            ''', (the_region, the_date, the_svg))
            self.cnxn.commit()
            action = 'inserted'
        except:
            cursor.execute('''
                SELECT the_svg FROM plot_by_date_v0
                WHERE the_region = :the_region AND the_date = :the_date
            ''', (the_region, the_date))
            res = cursor.fetchone()
            if res:
                current_json = res[0]
                if the_svg == current_json:
                    action = 'validated'
                else:
                    cursor.execute('''
                        UPDATE plot_by_date_v0
                        SET the_svg = :the_svg
                        WHERE the_region = :the_region AND the_date = :the_date
                    ''',
                    (the_svg, the_region, the_date))
                    action = 'updated'
                    self.cnxn.commit()
        finally:
            self.cnxn.close()
            return action


    def byhour_v0(self, datamodel: object)-> str:
        action = None
        cursor = self.cnxn.cursor()
        the_region = datamodel.region
        the_hour = datamodel.hour
        the_index = datamodel.index
        the_date = datamodel.date
        the_svg = datamodel.data
        try:
            cursor.execute('''
                INSERT INTO plot_by_hour_v0
                    (the_region, the_date, the_hour, the_index, the_svg) 
                VALUES
                    (:the_region, :the_date, :the_hour, :the_index, :the_svg)
            ''', (the_region, the_date, the_hour, the_index, the_svg))
            self.cnxn.commit()
            action = 'inserted'
        except:
            cursor.execute('''
                SELECT the_svg FROM plot_by_hour_v0
                WHERE the_region = :the_region
                  AND the_date = :the_date
                  AND the_hour = :the_hour
                  AND the_index = :the_index
            ''', (the_region, the_date, the_hour, the_index))
            res = cursor.fetchone()
            if res:
                current_json = res[0]
                if the_svg == current_json:
                    action = 'validated'
                else:
                    cursor.execute('''
                        UPDATE plot_by_hour_v0
                        SET the_svg = :the_svg
                        WHERE the_region = :the_region
                          AND the_date = :the_date
                          AND the_hour = :the_hour
                          AND the_index = :the_index
                    ''',
                    (the_svg, the_region, the_date, the_hour, the_index))
                    action = 'updated'
                    self.cnxn.commit()
        finally:
            self.cnxn.close()
            return action
