from cocuvida.sqldatabase import connect

QUERIES = {
    'insert_state': 'INSERT INTO state_schedule (plan_name, target_type, state_value) VALUES (?, ?, ?)',
    'insert_states_from_generator': 'INSERT INTO state_schedule (plan_name, target_type, state_value, state_time) VALUES (?, ?, ?, ?)',
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