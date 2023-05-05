from cocuvida.timehandle import isodates

from .calendar import Calendar
from .schedule import Schedule
from .target import Target


class ControlPlan:

    def __init__(self):
        self.calendar = dict()
        self.schedule = dict()
        self.target = dict()

    async def load_controlplan(self, controlplan: dict) -> str:
        plan_name = controlplan['name']
        self.calendar[plan_name] = Calendar(controlplan['calendar'])
        self.schedule[plan_name] = Schedule(controlplan['schedule'])
        self.target[plan_name]   = Target(controlplan['target'])
        return plan_name

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
        if await self.calendar[plan_name].is_included_weekday(isodate):
            return True
        return False

    async def generate_states(self, plan_name: str, isodate: str) -> list:
        if self.schedule == {} or self.target == {}:
            raise Exception('NoControlplanError: run ControlplanParser.load_controlplan(controlplan) before anything else')

        states = await self.schedule[plan_name].generate_states(isodate)
        for row in states:
            target_type = row[0]
            if await self.target[plan_name].is_included(target_type):
                state_status = 0 # target enabled (state will be published)
            else:
                state_status = 2 # target disabled (state will NOT be published)
            row.insert(0, plan_name)
            row.append(state_status)
        return states

    async def target_is_included(self, plan_name: str, target_type: str):
        return await self.target[plan_name].is_included(target_type)

    async def publish_state(self, plan_name: str, target_type: str, state_value: str) -> bool:
        if self.target == {}:
            raise Exception('NoControlplanError: run ControlplanParser.load_controlplan(controlplan) before anything else')

        res = await self.target[plan_name].publish_state(target_type, state_value)
        return res
