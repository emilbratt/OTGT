from cocuvida.timehandle import isodates

from . import calendar, schedule, target


class ControlPlan:

    def __init__(self):
        # controlplans go in this dictionary
        self.cp = dict()

    async def load_controlplan(self, controlplan: dict) -> None:
        plan_name = controlplan['name']
        self.cp[plan_name] = controlplan

    async def valid_state_types(self, states: list) -> bool:
        raise Exception('MethodNotImplemented')

    async def validate_controlplan(self) -> bool:
        raise Exception('MethodNotImplemented')

    async def is_operating_date(self, plan_name: str, isodate) -> bool:
        if self.cp == {}:
            raise Exception('NoControlplanError: run ControlplanParser.load_controlplan(controlplan) before anything else')

        cal = calendar.Entry(self.cp[plan_name]['calendar'])
        # from highest priority (excluded dates) -> to lowest priority (weekdays)
        if await cal.is_excluded_date(isodate):
            return False
        if await cal.is_included_date(isodate):
            return True
        if await cal.is_included_weekday(isodate):
            return True
        return False

    async def generate_states(self, plan_name: str, isodate: str) -> list:
        if self.cp == {}:
            raise Exception('NoControlplanError: run ControlplanParser.load_controlplan(controlplan) before anything else')

        schdl = schedule.Entry(self.cp[plan_name]['schedule'])
        states = await schdl.generate_states(isodate)
        for row in states:
            target_type = row[0]
            if self.cp[plan_name]['target'][target_type]['include_entry']:
                state_status = 0 # publishing enabled
            else:
                state_status = 2 # publishing disabled
            row.insert(0, plan_name)
            row.append(state_status)
        return states

    async def publish_state(self, plan_name: str, target_type: str, state_value: str,) -> bool:
        if self.cp == {}:
            raise Exception('NoControlplanError: run ControlplanParser.load_controlplan(controlplan) before anything else')

        trgt = target.Entry(self.cp[plan_name]['target'][target_type])
        res = await trgt.publish_state(target_type, state_value)
        return res