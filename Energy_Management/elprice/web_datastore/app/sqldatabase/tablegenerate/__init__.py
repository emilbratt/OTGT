# the_date -> YYYY-MM-DD
# the_region -> nordpool region (Molde, Kr.sand, DK1, FI)
TABLE_MAP = {
    'elspot_raw_v1':
    {
        'create': '''
            CREATE TABLE IF NOT EXISTS elspot_raw_v1 (
                the_date      NOT NULL PRIMARY KEY,
                the_json JSON NOT NULL
            );
        ''',
        'drop': 'DROP TABLE IF EXISTS elspot_raw_v1;',
    },

    'elspot_reshaped_v1':
    {
        'create': '''
            CREATE TABLE IF NOT EXISTS elspot_reshaped_v1 (
                the_region    NOT NULL,
                the_date      NOT NULL,
                the_json JSON NOT NULL,
                PRIMARY KEY (the_date, the_region)
            );
        ''',
        'drop': 'DROP TABLE IF EXISTS elspot_reshaped_v1;',
    },

    'plot_by_date_v1':
    {
        'create': '''
            CREATE TABLE IF NOT EXISTS plot_by_date_v1 (
                the_region   NOT NULL,
                the_date     NOT NULL,
                the_svg TEXT NOT NULL,
                PRIMARY KEY (the_region, the_date)
            );
        ''',
        'drop': 'DROP TABLE IF EXISTS plot_by_date_v1;',
    },

    'plot_by_quarter_v1':
    {
        'create': '''
            CREATE TABLE IF NOT EXISTS plot_by_quarter_v1 (
                the_region      NOT NULL,
                the_date        NOT NULL,
                the_hour    INT NOT NULL,
                the_quarter INT NOT NULL,
                the_index   INT NOT NULL,
                the_svg    TEXT NOT NULL,
                PRIMARY KEY (the_region, the_date, the_index)
            );
        ''',
        'drop': 'DROP TABLE IF EXISTS plot_by_quarter_v1;',
    },

    'sensor_by_date_v1':
    {
        'create': '''
            CREATE TABLE IF NOT EXISTS sensor_by_date_v1 (
                the_region    NOT NULL,
                the_date      NOT NULL,
                the_json JSON NOT NULL,
                PRIMARY KEY (the_region, the_date)
            );
        ''',
        'drop': 'DROP TABLE IF EXISTS sensor_by_date_v1;',
    },

}
