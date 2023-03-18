from cocuvida.sqldatabase import connect


QUERIES = {
    'insert_state': 'INSERT INTO state_schedule (plan_name, device_type, state_value) VALUES (?, ?, ?)',
    'insert_states_from_generator': 'INSERT INTO state_schedule (plan_name, device_type, state_value, state_timestamp) VALUES (?, ?, ?, ?)',
    'update_state': 'UPDATE state_schedule  SET state_value = ? WHERE plan_name = ? AND device_type AND state_timestamp = ?',
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
        #await generate_states(control_plan, isodate.today())
        action = 'insert'
    except Exception as e:
        action = f'ERROR: {__file__} {type(e)} {e}'
    finally:
        cnxn.close()
        return action