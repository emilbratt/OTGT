from cocuvida.timehandle import isodates

from .calendar import Calendar
from .schedule import Schedule
from .target import Target


class ControlPlan:

    def __init__(self):
        self.plan_names = set()
        self.calendar = dict()
        self.schedule = dict()
        self.target = dict()

    async def load_controlplan(self, controlplan: dict) -> bool:
        plan_name = controlplan['name']
        # target entry must always be included
        if 'target' not in controlplan:
            raise Exception('NoTargetInControlplan',plan_name )

        calendar_entry = {}
        schedule_entry = {}
        if 'calendar' in controlplan:
            calendar_entry = controlplan['calendar']
        if 'schedule' in controlplan:
            schedule_entry = controlplan['schedule']
        self.calendar[plan_name] = Calendar(calendar_entry)
        self.schedule[plan_name] = Schedule(schedule_entry)

        target_entry = controlplan['target']
        self.target[plan_name] = Target(target_entry)
        self.plan_names.add(plan_name)
        return True

    async def unload_controlplan(self, plan_name: str) -> bool:
        self.plan_names.discard(plan_name)
        self.calendar.pop(plan_name)
        self.schedule.pop(plan_name)
        self.target.pop(plan_name)
        return True

    async def get_plan_names(self):
        return self.plan_names

    async def valid_state_types(self, states: list) -> bool:
        raise Exception('MethodNotImplemented')

    async def validate_controlplan(self) -> bool:
        raise Exception('MethodNotImplemented')

    async def is_operating_date(self, plan_name: str, isodate) -> bool:
        if self.calendar == {}:
            raise Exception('NoControlplanError: run ControlplanParser.load_controlplan(controlplan) before anything else')

        # from highest priority (excluded dates) -> to lowest priority (weekdays)
        if await self.calendar[plan_name].is_excluded_date(isodate):
            return False
        if await self.calendar[plan_name].is_included_date(isodate):
            return True
        weekday = isodates.weekday_name_from_isodate(isodate)
        if await self.calendar[plan_name].is_excluded_weekday(weekday):
            return False
        if await self.calendar[plan_name].is_included_weekday(weekday):
            return True
        return False

    async def generate_states(self, plan_name: str, isodate: str) -> list:
        if self.schedule == {} or self.target == {}:
            raise Exception('NoControlplanError: run ControlplanParser.load_controlplan(controlplan) before anything else')

        states = await self.schedule[plan_name].generate_states(isodate)
        for row in states:
            target_type = row[0]
            if await self.target[plan_name].target_enabled(target_type):
                state_status = 0 # target enabled (state will be published)
            else:
                state_status = 2 # target disabled (state will NOT be published)
            row.insert(0, plan_name)
            row.append(state_status)
        return states

    async def target_enabled(self, plan_name: str, target_type: str):
        return await self.target[plan_name].target_enabled(target_type)

    async def publish_state(self, plan_name: str, target_type: str, state_value: str) -> bool:
        if self.target == {}:
            raise Exception('NoControlplanError: run ControlplanParser.load_controlplan(controlplan) before anything else')

        res = await self.target[plan_name].publish_state(target_type, state_value)
        return res

    async def list_targets(self, plan_name: str) -> list:
        return await self.target[plan_name].list_targets()
