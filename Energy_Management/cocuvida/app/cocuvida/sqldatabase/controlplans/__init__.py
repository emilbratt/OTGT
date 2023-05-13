from yaml import safe_load as yaml_safe_load
from io import StringIO

from cocuvida.timehandle import isodates, unix
from cocuvida.sqldatabase import connect, select_all, select_one_no_param


async def list_plan_names() -> list:
    query = 'SELECT plan_name FROM control_plans'
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute(query)
    plan_names = []
    for name in cursor:
        plan_names.append(name[0])
    cnxn.close()
    return plan_names

async def list_plan_names_greater_than_timestamp(timestamp: str) -> list:
    query = 'SELECT plan_name FROM control_plans WHERE last_updated > ?'
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute(query, [timestamp])
    plan_names = []
    for name in cursor:
        plan_names.append(name[0])
    cnxn.close()
    return plan_names

async def insert_control_plan(control_plan: str) -> str:
    insert_query = 'INSERT INTO control_plans (plan_name, plan_data, last_updated) VALUES (?, ?, ?)'
    update_query = 'UPDATE control_plans  SET plan_data = ?, last_updated = ?  WHERE plan_name = ?'
    action = str()
    last_updated = unix.int_timestamp()
    try:
        # load name and at the same time check if YAML parasble before inserting
        plan_name = yaml_safe_load(control_plan)['name']
    except Exception as e:
        action = f'ERROR: {__file__} MSG: Invalid yaml DESC: {type(e)} {e}'
        return action
    cnxn = connect()
    cursor = cnxn.cursor()
    try:
        cursor.execute(insert_query, [plan_name, control_plan, last_updated])
        cnxn.commit()
        action = 'insert'
    except:
        try:
            # if insert failed, most likely constraint -> update table instead
            cursor.execute(update_query, [control_plan, last_updated, plan_name])
            cnxn.commit()
            action = 'update'
        except Exception as e:
            action = f'ERROR: {__file__} {type(e)} {e}'
    finally:
        cnxn.close()
        return action

async def select_control_plan_by_plan_name(plan_name: str) -> dict:
    query = 'SELECT plan_data FROM control_plans WHERE plan_name = ?'
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute(query, [plan_name])
    res = cursor.fetchone()
    cnxn.close()
    if res == None:
        return {}
    return yaml_safe_load(res[0])

async def select_all_control_plans() -> dict:
    query = 'SELECT plan_data FROM control_plans'
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute(query)
    plans = {}
    for row in cursor:
        plan_data = yaml_safe_load(row[0])
        plan_name = plan_data['name']
        plans[plan_name] = plan_data
    cnxn.close()
    return plans

async def get_stringio_control_plan_by_name(plan_name: str) -> object:
    query = 'SELECT plan_data FROM control_plans WHERE plan_name = ?'
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute(query, [plan_name])
    res = cursor.fetchone()[0]
    cnxn.close()
    file_object = StringIO(res)
    file_data = file_object.read().encode()
    file_object.close()
    return file_data

async def delete_control_plan(plan_name: str) -> str:
    query = 'DELETE FROM control_plans WHERE plan_name = ?'
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

async def select_latest_modification_time() -> int:
    query = 'SELECT last_updated FROM control_plans ORDER BY last_updated DESC LIMIT 1'
    res = select_one_no_param(query)
    if res == None:
        # return 0 (new controlplans will have a value much higher anyway)
        return 0
    else:
        return int(res[0])
