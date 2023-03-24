class Entry:

    def __init__(self, schedule: dict):
        self.s = schedule

    async def generate_states(self, isodate: str):
        included_entry = None
        for entry in self.s:
            if self.s[entry]['include_entry']:
                included_entry = entry
        match included_entry:
            case 'elspot':
                from .elspot import Entry
            case 'sun':
                from .sun import Entry
            case 'time':
                from .time import Entry
            case None:
                raise Exception('MissingEntryInSchedule')
            case _:
                raise Exception('UnknownEntryInSchedule', included_entry)
        obj = Entry(self.s[included_entry])
        return await obj.generate_states(isodate)
