from yaml import safe_load as yaml_safe_load
from io import StringIO

from cocuvida.controlplanparser import ControlplanParser

from cocuvida.timehandle import isodates
from cocuvida.sqldatabase import connect, select_all

QUERIES = {
    'insert_control_plan': 'INSERT INTO control_plans (plan_name, plan_data, last_updated) VALUES (?, ?, ?)',
    'update_control_plan': 'UPDATE control_plans  SET plan_data = ?, last_updated = ?  WHERE plan_name = ?',
    'select_control_plan_by_plan_name': 'SELECT plan_data FROM control_plans WHERE plan_name = ?',
    'select_all_control_plans': 'SELECT plan_data FROM control_plans',
    'delete_control_plan': 'DELETE FROM control_plans WHERE plan_name = ?',
    'list_plan_names': 'SELECT plan_name FROM control_plans',
    'list_plan_names_greater_than_timestamp': 'SELECT plan_name FROM control_plans WHERE last_updated > ?',
    'select_latest_modification_time': 'SELECT last_updated FROM control_plans ORDER BY last_updated DESC LIMIT 1',
}


async def list_plan_names() -> list:
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute(QUERIES['list_plan_names'])
    plan_names = []
    for name in cursor:
        plan_names.append(name[0])
    cnxn.close()
    return plan_names

async def list_plan_names_greater_than_timestamp(timestamp: str) -> list:
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute(QUERIES['list_plan_names_greater_than_timestamp'], [timestamp])
    plan_names = []
    for name in cursor:
        plan_names.append(name[0])
    cnxn.close()
    return plan_names

async def insert_control_plan(control_plan: str) -> str:
    action = str()
    timestamp = isodates.timestamp_now_round('second')
    try:
        # load name and at the same time check if YAML parasble before inserting
        plan_name = yaml_safe_load(control_plan)['name']
    except Exception as e:
        action = f'ERROR: {__file__} MSG: Invalid yaml DESC: {type(e)} {e}'
        return action
    cnxn = connect()
    cursor = cnxn.cursor()
    try:
        cursor.execute(QUERIES['insert_control_plan'], [plan_name, control_plan, timestamp])
        cnxn.commit()
        action = 'insert'
    except:
        try:
            # if insert failed, most likely constraint -> update table instead
            cursor.execute(QUERIES['update_control_plan'], [control_plan, timestamp, plan_name])
            cnxn.commit()
            action = 'update'
        except Exception as e:
            action = f'ERROR: {__file__} {type(e)} {e}'
    finally:
        cnxn.close()
        return action

async def select_control_plan_by_plan_name(plan_name: str) -> dict:
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute(QUERIES['select_control_plan_by_plan_name'], [plan_name])
    res = cursor.fetchone()
    cnxn.close()
    return yaml_safe_load(res[0])

async def select_all_control_plans() -> dict:
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute(QUERIES['select_all_control_plans'])
    plans = {}
    for row in cursor:
        plan_data = yaml_safe_load(row[0])
        plan_name = plan_data['name']
        plans[plan_name] = plan_data
    cnxn.close()
    return plans

async def get_stringio_control_plan_by_name(plan_name: str) -> object:
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute(QUERIES['select_control_plan_by_plan_name'], [plan_name])
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
    except Exception as e:
        action = f'ERROR: {__file__} {type(e)} {e}'
    finally:
        cnxn.close()
        return action

async def select_latest_modification_time() -> str:
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute(QUERIES['select_latest_modification_time'])
    res = cursor.fetchone()
    cnxn.close()
    return res[0]