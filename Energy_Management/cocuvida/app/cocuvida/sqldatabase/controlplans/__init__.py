from yaml import dump as yaml_dump
from yaml import safe_load as yaml_safe_load
from io import StringIO

from cocuvida.sqldatabase import connect


QUERIES = {
    'insert_control_plan': 'INSERT INTO control_plans (plan_name, plan_data) VALUES (?, ?)',
    'update_control_plan': 'UPDATE control_plans  SET plan_data = ?  WHERE plan_name = ?',
    'show_control_plan': 'SELECT plan_data FROM control_plans WHERE plan_name = ?',
    'delete_control_plan': 'DELETE FROM control_plans WHERE plan_name = ?',
    'list_plan_names': 'SELECT plan_name FROM control_plans',
}

async def list_plan_names() -> list:
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute(QUERIES['list_plan_names'])
    res = cursor.fetchall()
    cnxn.close()
    return res

async def insert_control_plan(control_plan: dict) -> str:
    action = ''
    plan_data = yaml_safe_load(control_plan)
    plan_name = plan_data['name']
    cnxn = connect()
    cursor = cnxn.cursor()
    try:
        cursor.execute(QUERIES['insert_control_plan'], [plan_name, control_plan])
        cnxn.commit()
        action = 'insert'
    except:
        try:
            # if insert failed, most likely constraint -> update table instead
            cursor.execute(QUERIES['update_control_plan'], [control_plan, plan_name])
            cnxn.commit()
            action = 'update'
        except Exception as e:
            action = f'ERROR: {__file__} {type(e)} {e}'
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

async def get_stringio_control_plan(plan_name: str) -> object:
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
    except Exception as e:
        action = f'ERROR: {__file__} {type(e)} {e}'
    finally:
        cnxn.close()
        return action
