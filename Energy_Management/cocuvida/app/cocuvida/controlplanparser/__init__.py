from cocuvida.timehandle import isodates

from .sections import calendar, schedule, target


class ControlplanParser:

    def __init__(self):
        self.cp = {}
        self.info = str()

    async def load_controlplan(self, controlplan: dict) -> None:
        self.cp[controlplan['name']] = controlplan

    async def valid_state_types(self, states: list) -> bool:
        raise Exception('MethodNotImplemented')

    async def validate_controlplan(self) -> bool:
        raise Exception('MethodNotImplemented')

    async def date_is_operating_date(self, plan_name: str, isodate) -> bool:
        if self.cp == None:
            raise Exception('NoControlplanError: run ControlplanParser.load_controlplan(controlplan) before anything else')

        c = calendar.Entry(self.cp[plan_name]['calendar'])
        # from highest priority (excluded dates) -> to lowest priority (weekdays)
        if await c.date_is_excluded_date(isodate):
            return False
        if await c.date_is_included_date(isodate):
            return True
        if await c.date_is_included_weekday(isodate):
            return True
        return False

    async def generate_states(self, plan_name: str, isodate: str) -> list:
        if self.cp == None:
            raise Exception('NoControlplanError: run ControlplanParser.load_controlplan(controlplan) before anything else')

        obj = schedule.Entry(self.cp[plan_name]['schedule'])
        states = await obj.generate_states(isodate)
        # insert the plan name in every record as first colummn and state_status as last (matches db columns)
        # changes makes each row look like this: [plan_name, target_type, state_value, state_time, state_status]
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
        if self.cp == None:
            raise Exception('NoControlplanError: run ControlplanParser.load_controlplan(controlplan) before anything else')

        target_entry = self.cp[plan_name]['target'][target_type]
        target_entry_obj = target.Entry(target_entry)
        res = await target_entry_obj.publish_state(target_type, state_value)
        return res