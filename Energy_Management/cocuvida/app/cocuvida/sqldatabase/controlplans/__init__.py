import sqlite3
import json
from yaml import dump as yaml_dump
from yaml import safe_load as yaml_safe_load
from io import StringIO

from cocuvida.sqldatabase import connect


QUERIES = {
    'insert_control_plan': 'INSERT INTO switch_control_plans (plan_name, plan_data) VALUES (?, ?)',
    'update_control_plan': 'UPDATE switch_control_plans  SET plan_data = ?  WHERE plan_name = ?',
    'show_control_plan': 'SELECT plan_data FROM switch_control_plans WHERE plan_name = ?',
    'delete_control_plan': 'DELETE FROM switch_control_plans WHERE plan_name = ?',
    'list_plan_names': 'SELECT plan_name FROM switch_control_plans',
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

async def select_control_plan(plan_name: str) -> dict:
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
