import asyncio
from datetime import datetime

from cocuvida.controlplanparser import ControlplanParser
from cocuvida.sqldatabase import (controlplans as sql_controlplans,
                                  stateschedule as sql_stateschedule)
from cocuvida.timehandle import isodates, timeofday


class PublishStates:
    '''
        load states from SQL table state_schedule and publish
    '''
    def __init__(self):
        self.init_time = isodates.timestamp_now()
        self.cpparser = None
        self.on_startup_ok = False
        self.last_updated_controlplan_timestamp = None

    async def on_startup(self) -> None:
        self.cpparser = ControlplanParser()
        self.last_updated_controlplan_timestamp = await sql_controlplans.select_latest_modification_time()
        res = await sql_controlplans.select_all_control_plans()
        for plan_data in res.values():
            await self.cpparser.load_controlplan(plan_data)
        self.on_startup_ok = True

    async def update_controlplans(self):
        if not self.on_startup_ok:
            raise Exception('OnStartupError: run WorkerGenerate.on_startup() before anything else')
        res = await sql_controlplans.list_plan_names_greater_than_timestamp(self.last_updated_controlplan_timestamp)
        self.last_updated_controlplan_timestamp = await sql_controlplans.select_latest_modification_time()
        for plan_name in res:
            # this will update (or add new) controlplans to the ControlplanParser (if any rows)
            plan_data = await sql_controlplans.select_control_plan_by_plan_name(plan_name)
            await self.cpparser.load_controlplan(plan_data)

    async def publish_current_states(self) -> None:
        if not self.on_startup_ok:
            raise Exception('OnStartupError: run WorkerGenerate.on_startup() before anything else')

        # load unpublished states for this time of day 'HH:MM'
        timestamp = isodates.timestamp_now_round('minute')
        res = await sql_stateschedule.select_unpublished_for_timestamp(timestamp)
        tasks = []
        for row in res:
            plan_name = row[0]
            target_type = row [1]
            state_value = row[2]
            state_time = row[3]
            rowid = row[4]
            print('Publish:', plan_name, target_type, state_value)
            res = await self.cpparser.publish_state(plan_name, target_type, state_value)
            if res:
                # publish OK
                state_status = 1
            else:
                # publish failed
                state_status = 3
            await sql_stateschedule.update_state_status_by_rowid(rowid, state_status)