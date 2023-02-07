import sqlite3

class Tables:

    # TABLE_MAP:
    # hardcoding might seem dum, especially since drop and check
    # basically are the same queries; but this map also serve the
    # purpose of documenting the schema with a quick glance
    TABLE_MAP = {
        'elspot_raw_v0':
        {
            'create': '''
                CREATE TABLE IF NOT EXISTS elspot_raw_v0 (
                    the_date      NOT NULL PRIMARY KEY,
                    the_json JSON NOT NULL
                );
            ''',
            'drop': 'DROP TABLE IF EXISTS elspot_raw_v0;',
            'check': '''
                SELECT COUNT(name) FROM sqlite_master
                WHERE type='table' AND name='elspot_raw_v0';
            ''',
        },

        'elspot_reshaped_v0':
        {
            'create': '''
                CREATE TABLE IF NOT EXISTS elspot_reshaped_v0 (
                    the_region    NOT NULL,
                    the_date      NOT NULL,
                    the_json JSON NOT NULL,
                    PRIMARY KEY (the_date, the_region)
                );
            ''',
            'drop': 'DROP TABLE IF EXISTS elspot_reshaped_v0;',
            'check': '''
                SELECT COUNT(name) FROM sqlite_master
                WHERE type='table' AND name='elspot_raw_v0';
            ''',
        },

        'elspot_reshaped_v1':
        {
            'create': '''
                CREATE TABLE IF NOT EXISTS elspot_reshaped_v1 (
                    the_date      NOT NULL,
                    the_json JSON NOT NULL,
                    PRIMARY KEY (the_date)
                );
            ''',
            'check': '''
                SELECT COUNT(name) FROM sqlite_master
                WHERE type='table' AND name='elspot_reshaped_v1';
            ''',
            'drop': 'DROP TABLE IF EXISTS elspot_reshaped_v1;',
        },

        'plot_by_date_v0':
        {
            'create': '''
                CREATE TABLE IF NOT EXISTS plot_by_date_v0 (
                    the_region   NOT NULL,
                    the_date     NOT NULL,
                    the_svg TEXT NOT NULL,
                    PRIMARY KEY (the_region, the_date)
                );
            ''',
            'check': '''
                SELECT COUNT(name) FROM sqlite_master
                WHERE type='table' AND name='plot_by_date_v0';
            ''',
            'drop': 'DROP TABLE IF EXISTS plot_by_date_v0;',
        },

        'plot_by_hour_v0':
        {
            'create': '''
                CREATE TABLE IF NOT EXISTS plot_by_hour_v0 (
                    the_region      NOT NULL,
                    the_date        NOT NULL,
                    the_hour    INT NOT NULL,
                    the_index   INT NOT NULL,
                    the_svg    TEXT NOT NULL,
                    PRIMARY KEY (the_region, the_date, the_hour, the_index)
                );
            ''',
            'check': '''
                SELECT COUNT(name) FROM sqlite_master
                WHERE type='table' AND name='plot_by_hour_v0';
            ''',
            'drop': 'DROP TABLE IF EXISTS plot_by_hour_v0;',
        },

        'sensor_by_date_v0':
        {
            'create': '''
                CREATE TABLE IF NOT EXISTS sensor_by_date_v0 (
                    the_region    NOT NULL,
                    the_date      NOT NULL,
                    the_json JSON NOT NULL,
                    PRIMARY KEY (the_region, the_date)
                );
            ''',
            'check': '''
                SELECT COUNT(name) FROM sqlite_master
                WHERE type='table' AND name='sensor_by_date_v0';
            ''',
            'drop': 'DROP TABLE IF EXISTS sensor_by_date_v0;',
        },

        'test':
        {
            'create': '''
                CREATE TABLE IF NOT EXISTS test (
                    the_region    NOT NULL,
                    the_date      NOT NULL,
                    the_json JSON NOT NULL,
                    PRIMARY KEY (the_region, the_date)
                );
            ''',
            'check': '''
                SELECT COUNT(name) FROM sqlite_master
                WHERE type='table' AND name='test';
            ''',
            'drop': 'DROP TABLE IF EXISTS test;',
        },
    }

    def __init__(self, databasefile: str):
         self.databasefile = databasefile

    def run(self, table: str, operation: str) -> dict:
        namespace = __file__ + '.Tables'
        result = { 'table': table, 'operation': operation }
        cnxn = sqlite3.connect(self.databasefile)
        cursor = cnxn.cursor()
        try:
            query = self.TABLE_MAP[table][operation]
        except KeyError:
            result['error'] = 'might not be defined in ' + namespace + '.TABLE_MAP'
            cnxn.close()
            return result

        try:
            cursor.execute(query)
        except sqlite3.OperationalError as e:
            result['error'] = 'maybe syntax error in ' + namespace + '.TABLE_MAP'
            result['sqlite3OperationalError'] = e
            result['query_dump'] = query
            cnxn.close()
            return result

        match operation:
            case 'check':
                result['exists'] = (cursor.fetchone()[0] == 1)
            case 'create':
                cnxn.commit()
                result['created'] = True
            case 'drop':
                cnxn.commit()
                result['dropped'] = True

        cnxn.close()
        return result
