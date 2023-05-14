from cocuvida import libcontrolplan
from cocuvida.sqldatabase import controlplans as sql_controlplans
from cocuvida.sqldatabase import stateschedule as sql_stateschedule
from cocuvida.timehandle import isodates, timeofday


class Schedule:
    def __init__(self):
        self.cp_obj = libcontrolplan.ControlPlan()
        self.last_updated_controlplan_unix_ts = 0
        self.generated_for_tomorrow = False

    async def load_new_controlplans(self) -> None:
        unix_time = await sql_controlplans.select_latest_modification_time()
        if unix_time > self.last_updated_controlplan_unix_ts:
            plan_names = await sql_controlplans.list_plan_names_greater_than_timestamp(self.last_updated_controlplan_unix_ts)
            self.last_updated_controlplan_unix_ts = unix_time
            for plan_name in plan_names:
                # update or add new controlplans
                controlplan = await sql_controlplans.select_control_plan_by_plan_name(plan_name)
                await self.cp_obj.load_controlplan(controlplan)
                # clear all future states (if exists) for new controlplans
                tomorrow = isodates.today_plus_days(1)
                today = isodates.today()
                await sql_stateschedule.delete_states_for_plan_name_and_date(plan_name, today)
                await sql_stateschedule.delete_states_for_plan_name_and_date(plan_name, tomorrow)
                # generate new states (if a schedule is included)
                states = await self.cp_obj.generate_states(plan_name, today)
                await sql_stateschedule.insert_states_from_generator(states)
                states = await self.cp_obj.generate_states(plan_name, tomorrow)
                await sql_stateschedule.insert_states_from_generator(states)

    async def unload_controlplans(self) -> None:
        plan_names_loaded = await self.cp_obj.get_plan_names()
        plan_names_database = await sql_controlplans.list_plan_names()
        unload = []
        for plan_name in plan_names_loaded:
            if plan_name not in plan_names_database:
                unload.append(plan_name)
        for plan_name in unload:
            await self.cp_obj.unload_controlplan(plan_name)

    async def generate_states_for_tomorrow(self) -> None:
        if timeofday.is_before_time(14, 0):
            self.generated_for_tomorrow = False
            return None
        if self.generated_for_tomorrow:
            return None
        plan_names = await self.cp_obj.get_plan_names()
        isodate = isodates.today_plus_days(1)
        for plan_name in plan_names:
            await sql_stateschedule.delete_states_for_plan_name_and_date(plan_name, isodate)
            if await self.cp_obj.is_operating_date(plan_name, isodate):
                states = await self.cp_obj.generate_states(plan_name, isodate)
                await sql_stateschedule.insert_states_from_generator(states)
        self.generated_for_tomorrow = True

    async def publish_current_states(self) -> None:
        timestamp = isodates.timestamp_now_round('minute')
        states = await sql_stateschedule.select_non_published_states_for_timestamp(timestamp)
        tasks = []
        for row in states:
            plan_name = row[0]
            target_type = row[1]
            state_value = row[2]
            state_time = row[3]
            rowid = row[4]
            published = await self.cp_obj.publish_state(plan_name, target_type, state_value)
            if published:
                context = 'published'
            else:
                context = 'published failed'
            state_status = sql_stateschedule.STATUS_ENUMS.index(context)
            await sql_stateschedule.update_state_status_by_rowid(rowid, state_status)
            print(f'CONTROLPLAN: {context} {plan_name} {target_type} {state_value}')
