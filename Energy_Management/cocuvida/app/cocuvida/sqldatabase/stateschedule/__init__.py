from cocuvida.sqldatabase import connect, select_all
from cocuvida.timehandle import isodates

QUERIES = {
    'insert_states_from_generator': 'INSERT INTO state_schedule (plan_name, target_type, state_value, state_time, state_status) VALUES (?, ?, ?, ?, ?)',
    'delete_states_for_plan_name_and_date': 'DELETE FROM state_schedule WHERE plan_name = ? AND DATE(state_time) = ?',
}


async def insert_states_from_generator(rows: list) -> str:
    '''
        insert new state schedule (one row from generate_states unit)
    '''
    action = str()
    cnxn = connect()
    cursor = cnxn.cursor()
    try:
        cursor.executemany(QUERIES['insert_states_from_generator'], rows)
        cnxn.commit()
        action = 'insert'
    except Exception as e:
        action = f'ERROR: {__file__} {type(e)} {e}'
    finally:
        cnxn.close()
        return action

async def delete_states_for_plan_name_and_date(plan_name: str, isodate: str):
    action = str()
    cnxn = connect()
    cursor = cnxn.cursor()
    try:
        cursor.execute(QUERIES['delete_states_for_plan_name_and_date'], [plan_name, isodate])
        cnxn.commit()
        action = 'delete'
    except Exception as e:
        action = f'ERROR: {__file__} {type(e)} {e}'
    finally:
        cnxn.close()
        return action

async def select_current_states() -> list:
    '''
        timestamp is in the form '%Y-%m-%d %H:%M' e.g. '2023-06-17 12:00'
        this means that as long as the date and HH:MM matches (seconds are not counted) we return rows
        returns empty list if no match is found
    '''
    query = '''
        SELECT plan_name, target_type, state_value, state_time
        FROM state_schedule
        WHERE state_time = ?
    '''
    ts = isodates.timestamp_now_round('minute')
    ts = '2023-06-17 12:00'
    return select_all(query, [ts])

async def select_published_states_for_date(isodate: str) -> list:
    '''
        returns by passed date an ordered list of already published state values (newest first)
    '''
    query = '''
        SELECT plan_name, target_type, state_value, state_time
        FROM state_schedule
        WHERE state_status = 1
        AND DATE(state_time) = ?
        ORDER BY state_time ASC
    '''
    return select_all(query, [isodate])

async def select_non_published_states_for_date(isodate: str) -> list:
    '''
        returns by passed date an ordered list of non published state values (newest first)
    '''
    query = '''
        SELECT plan_name, target_type, state_value, state_time
        FROM state_schedule
        WHERE state_status = 0
        AND DATE(state_time) = ?
        ORDER BY state_time ASC
    '''
    return select_all(query, [isodate])

async def select_non_published_states_today() -> list:
    '''
        returns ordered list of todays non published state values (newest first)
    '''
    query = '''
        SELECT plan_name, target_type, state_value, state_time
        FROM state_schedule
        WHERE state_status = 0
        AND DATE(state_time) = ?
        ORDER BY state_time ASC
    '''
    return select_all(query, [isodates.today()])

async def select_unpublished_for_timestamp(timestamp: str) -> list:
    '''
        returns all within the window of whole minute (X mark) -> YYYY-MM-DD HH:MM:XX 
    '''
    # uses SQL function STRFTIME() to extract 'YYYY-MM-DD HH' (excluding minutes) from date
    query = '''
        SELECT plan_name, target_type, state_value, state_time, rowid
        FROM state_schedule
        WHERE state_status = 0
        AND STRFTIME('%Y-%m-%d %H:%M', state_time) = STRFTIME('%Y-%m-%d %H:%M', ?)
        ORDER BY state_time ASC
    '''
    #return select_all(query, [isodates.timestamp_now()])
    return select_all(query, [timestamp])

async def update_state_status_by_rowid(rowid: int, state_status: int) -> bool:
    '''
        0 = not published
        1 = is published
        2 = target disabled
        3 = publish failed
        returns all within the window of whole minute (X mark) -> YYYY-MM-DD HH:MM:XX 
    '''
    query = '''
        UPDATE state_schedule
        SET state_status = ?
        WHERE rowid = ?
    '''
    action = str()
    cnxn = connect()
    cursor = cnxn.cursor()
    try:
        cursor.execute(query, [state_status, rowid])
        cnxn.commit()
        action = 'update'
    except Exception as e:
        action = f'ERROR: {__file__} {type(e)} {e}'
    finally:
        cnxn.close()
        return action