from cocuvida.sqldatabase import connect, select_all
from cocuvida.timehandle import isodates

STATUS_ENUMS = ['not published', 'published', 'target disabled', 'publish failed']


async def insert_states_from_generator(rows: list) -> str:
    '''
        insert new state schedule (one row from generate_states unit)
    '''
    query = '''
        INSERT INTO state_schedule
            (plan_name, target_type, state_value, state_time, state_status)
        VALUES
            (?, ?, ?, ?, ?)
    '''
    action = str()
    cnxn = connect()
    cursor = cnxn.cursor()
    try:
        cursor.executemany(query, rows)
        cnxn.commit()
        action = 'insert'
    except Exception as e:
        action = f'ERROR: {__file__} {type(e)} {e}'
        print(action)
    finally:
        cnxn.close()
        return action

async def delete_states_for_plan_name(plan_name: str) -> str:
    query = '''
        DELETE FROM state_schedule
        WHERE plan_name = ?
    '''
    action = str()
    cnxn = connect()
    cursor = cnxn.cursor()
    try:
        cursor.execute(query, [plan_name])
        cnxn.commit()
        action = 'delete'
    except Exception as e:
        action = f'ERROR: {__file__} {type(e)} {e}'
    finally:
        cnxn.close()
        return action

async def delete_states_for_plan_name_and_date(plan_name: str, isodate: str) -> str:
    query = '''
        DELETE FROM state_schedule
        WHERE plan_name = ? AND DATE(state_time) = ?
    '''
    action = str()
    cnxn = connect()
    cursor = cnxn.cursor()
    try:
        cursor.execute(query, [plan_name, isodate])
        cnxn.commit()
        action = 'delete'
    except Exception as e:
        action = f'ERROR: {__file__} {type(e)} {e}'
    finally:
        cnxn.close()
        return action

async def select_published_states_for_date(isodate: str) -> list[list]:
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

async def select_non_published_states_for_date(isodate: str) -> list[list]:
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

async def select_non_published_states_today() -> list[list]:
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

async def select_non_published_states_for_timestamp(timestamp: str) -> list[list]:
    '''
        returns all within the window of a minute
        if date-time is 2022-01-01 13:12:43, returns all within time 2022-01-01 13:12
    '''
    query = '''
        SELECT plan_name, target_type, state_value, state_time, rowid
        FROM state_schedule
        WHERE state_status = 0
        AND STRFTIME('%Y-%m-%d %H:%M', state_time) = STRFTIME('%Y-%m-%d %H:%M', ?)
        ORDER BY state_time ASC
    '''
    return select_all(query, [timestamp])

async def select_non_published_states_for_date(isodate: str) -> list[list]:
    '''
        returns all rows for that date
    '''
    query = '''
        SELECT plan_name, target_type, state_value, state_time, rowid
        FROM state_schedule
        WHERE state_status = 0
        AND DATE(state_time) = ?
        ORDER BY state_time ASC
    '''
    return select_all(query, [isodate])

async def update_state_status_by_rowid(rowid: int, state_status: int) -> str:
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

async def select_all_states_today_for_plan_name(plan_name: str) -> list[list]:
    query = '''
        SELECT plan_name, target_type, state_value, state_time, state_status, rowid
        FROM state_schedule
        WHERE plan_name = ?
        AND STRFTIME('%Y-%m-%d', state_time) >= STRFTIME('%Y-%m-%d', ?)
        ORDER BY target_type, state_time ASC
    '''
    return select_all(query, [plan_name, isodates.today()])

async def select_all_states_for_date_and_plan_name(isodate: str, plan_name: str) -> list[list]:
    query = '''
        SELECT plan_name, target_type, state_value, state_time, state_status, rowid
        FROM state_schedule
        WHERE plan_name = ?
        AND STRFTIME('%Y-%m-%d', state_time) = STRFTIME('%Y-%m-%d', ?)
        ORDER BY target_type, state_time ASC
    '''
    timestamp = isodates.today()
    return select_all(query, [plan_name, isodate])
