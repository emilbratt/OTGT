import sqlite3
import json

from cocuvida.sqldatabase import connect


QUERIES = {
    'insert': 'INSERT INTO switch_control_plans (plan_name, plan_data) VALUES (?, ?)',
    'update': 'UPDATE switch_control_plans  SET plan_data = ?  WHERE plan_name = ?',
    'select': 'SELET * FROM deswitch_control_plansvices WHERE plan_name = ?',
    'select_all': 'SELECT * FROM deswitch_control_plansvices',
    'delete': 'DELETE FROM switch_control_plans WHERE plan_name = ?',
    'delete_all': 'DELETE FROM switch_control_plans',
}


async def insert_control_plan(control_plan: dict):
    plan_name = control_plan['name']
    plan_data = json.dumps(control_plan)

    cnxn = connect()
    cursor = cnxn.cursor()
    action = None
    try:
        cursor.execute(QUERIES['insert'], [plan_name, plan_data])
        cnxn.commit()
        action = 'insert'
    except sqlite3.IntegrityError:
        cursor.execute(QUERIES['update'], [plan_data, plan_name])
        cnxn.commit()
        action = 'update'
    finally:
        cnxn.close()
        return action
