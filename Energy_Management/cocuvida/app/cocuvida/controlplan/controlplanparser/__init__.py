import yaml

from cocuvida.timehandle import isodates

from .sections import calendar, schedule


class ControlplanParser:

    def __init__(self, controlplan: str):
        '''
            load YAML string version of control plan
        '''
        self.cp = yaml.safe_load(controlplan)
        self.info = str()

    async def get_name(self):
        return self.cp['name']

    async def valid_state_types(self, states: list) -> bool:
        raise Exception('MethodNotImplemented')

    async def validate_controlplan(self) -> bool:
        raise Exception('MethodNotImplemented')

    async def date_is_operating_date(self, isodate) -> bool:
        c = calendar.Entry(self.cp['calendar'])
        # from highest priority (excluded dates) -> to lowest priority (weekdays)
        if await c.date_is_excluded_date(isodate):
            return False
        if await c.date_is_included_date(isodate):
            return True
        if await c.date_is_included_weekday(isodate):
            return True
        return False

    async def generate_states(self, isodate: str) -> list:
        obj = schedule.Entry(self.cp['schedule'])
        states = await obj.generate_states(isodate)
        # insert the plan name in every record as first colummn
        for row in states:
            row.insert(0, self.cp['name'])
        return states
