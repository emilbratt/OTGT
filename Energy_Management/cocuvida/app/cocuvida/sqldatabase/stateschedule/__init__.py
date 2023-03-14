import sqlite3
# from yaml import dump as yaml_dump
# from yaml import safe_load as yaml_safe_load
#from io import StringIO

from cocuvida.sqldatabase import connect

# plan_name
# state_value
# state_timestamp

QUERIES = {
    'insert_state': 'INSERT INTO state_schedule (plan_name, state_value) VALUES (?, ?)',
    'insert_state_and_timestamp': 'INSERT INTO state_schedule (plan_name, state_value, state_timestamp) VALUES (?, ?, ?)',
    'update_state': 'UPDATE state_schedule  SET plan_data = ?  WHERE plan_name = ?',
    'show_state': 'SELECT plan_data FROM state_schedule WHERE plan_name = ? AND state_timestamp = ?',
    'delete_state': 'DELETE FROM state_schedule WHERE plan_name = ? AND state_timestamp = ?',
    'list_states': 'SELECT plan_name FROM state_schedule',
}

async def list_plan_names() -> list:
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute(QUERIES['list_plan_names'])
    res = cursor.fetchall()
    cnxn.close()
    return res

async def insert_control_plan(control_plan: dict) -> str:
    plan_data = yaml_safe_load(control_plan)
    plan_name = plan_data['name']
    cnxn = connect()
    cursor = cnxn.cursor()
    action = ''
    try:
        cursor.execute(QUERIES['insert_control_plan'], [plan_name, control_plan])
        cnxn.commit()
        action = 'insert'
    except sqlite3.IntegrityError:
        # if record with plan_name exist, update table instead
        cursor.execute(QUERIES['update_control_plan'], [control_plan, plan_name])
        cnxn.commit()
        action = 'update'
    finally:
        cnxn.close()
        return action

async def get_control_plan(plan_name: str) -> dict:
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute(QUERIES['show_control_plan'], [plan_name])
    res = cursor.fetchone()
    cnxn.close()
    return yaml_safe_load(res[0])

async def download_control_plan(plan_name: str) -> object:
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute(QUERIES['show_control_plan'], [plan_name])
    res = cursor.fetchone()[0]
    cnxn.close()
    file_object = StringIO(res)
    file_data = file_object.read().encode()
    file_object.close()
    return file_data

async def delete_control_plan(plan_name: str) -> str:
    cnxn = connect()
    cursor = cnxn.cursor()
    try:
        cursor.execute(QUERIES['delete_control_plan'], [plan_name])
        cnxn.commit()
        action = 'delete'
    except:
        action = ''
    finally:
        cnxn.close()
        return action
