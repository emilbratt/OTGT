from datetime import datetime

from cocuvida.controlplanparser import ControlplanParser
from cocuvida.sqldatabase import (controlplans as sql_controlplans,
                                  stateschedule as sql_stateschedule)

from cocuvida.timehandle import (isodates, timeofday)


class WorkerGenerate:
    '''
        generate states and insert into SQL table state_schedule
    '''
    def __init__(self):
        self.init_time = isodates.timestamp_now()
        self.on_startup_ok = False
        self.generate_for_next_day_check = None
        self.last_updated_controlplan_timestamp = None

    async def on_startup(self) -> None:
        self.generate_for_next_day_check = False
        self.last_updated_controlplan_timestamp = await sql_controlplans.select_latest_modification_time()
        self.on_startup_ok = True

    async def generate_for_all_controlplans(self, isodate: str) -> None:
        if not self.on_startup_ok:
            raise Exception('OnStartupError: run WorkerGenerate.on_startup() before anything else')

        print(f'generating for all controlplans with date {isodate}')
        cp = ControlplanParser()
        controlplans = await sql_controlplans.select_all_control_plans()
        for plan_name, plan_data in controlplans.items():
            await cp.load_controlplan(plan_data)
            await sql_stateschedule.delete_states_for_plan_name_and_date(plan_name, isodate)
            if await cp.date_is_operating_date(isodate):
                states = await cp.generate_states(isodate)
                await sql_stateschedule.insert_states_from_generator(states)

    async def generate_for_new_controlplans(self) -> None:
        '''
            on startup, we conserved the latest update timestamp for controlplan
            we stored the timestamp in self.last_updated_controlplan_timestamp
            we use this to check if threre are any new controlplans
            if there are, we generate states for today
            if we are passed 14:00 we generate for tomorrow as well
        '''
        if not self.on_startup_ok:
            raise Exception('OnStartupError: run WorkerGenerate.on_startup() before anything else')

        res = await sql_controlplans.list_plan_names_greater_than_timestamp(self.last_updated_controlplan_timestamp)
        if res == []:
            return
        self.last_updated_controlplan_timestamp = await sql_controlplans.select_latest_modification_time()
        cp = ControlplanParser()
        isodate_today = isodates.today()
        isodate_tomorrow = isodates.today_plus_days(1)
        is_passed_that_time = timeofday.is_passed_time(14, 0)
        for plan_name in res:
            print(f'generating for new controlplan {plan_name} with date {isodate_today}')
            plan_data = await sql_controlplans.select_control_plan_by_plan_name(plan_name)
            await cp.load_controlplan(plan_data)
            await sql_stateschedule.delete_states_for_plan_name_and_date(plan_name, isodate_today)
            if await cp.date_is_operating_date(isodate_today):
                states = await cp.generate_states(isodate_today)
                await sql_stateschedule.insert_states_from_generator(states)

            if is_passed_that_time:
                print(f'generating for new controlplan {plan_name} with date {isodate_tomorrow}')
                await sql_stateschedule.delete_states_for_plan_name_and_date(plan_name, isodate_tomorrow)
                if await cp.date_is_operating_date(isodate_tomorrow):
                    states = await cp.generate_states(isodate_tomorrow)
                    await sql_stateschedule.insert_states_from_generator(states)

    async def is_ready_to_generate_for_tomorrow(self) -> bool:
        '''
            checks if after 14:00
            checks if this has run more than once after 14:00 this day
            returns True if states are ready to be generated
            returns False if not

            logic deciding this is found in this method
        '''
        if not self.on_startup_ok:
            raise Exception('OnStartupError: run WorkerGenerate.on_startup() before anything else')

        # if time now before 14:00
        if timeofday.is_before_time(14, 0):
            self.generate_for_next_day_check = False
            return False
        # if we have already checked today and time was after 14:00
        if self.generate_for_next_day_check:
            return False
        # time is after 14:00 -> set checked today = True and return True
        self.generate_for_next_day_check = True
        return True
