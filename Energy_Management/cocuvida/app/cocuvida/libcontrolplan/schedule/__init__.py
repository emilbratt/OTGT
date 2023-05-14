from . import elspot, sun, time

from .const import IMPLEMENTED_SCHEULE_ENTRIES


class Schedule:

    def __init__(self, schedule_entry: dict):
        self.schedule_entry = schedule_entry

    async def generate_states(self, isodate: str) -> list:
        if self.schedule_entry == {}:
            return []
        schedule_entry = None
        for schedule in IMPLEMENTED_SCHEULE_ENTRIES:
            if schedule in self.schedule_entry:
                schedule_entry = schedule
        match schedule_entry:
            case 'elspot':
                return await elspot.generate_states(self.schedule_entry[schedule_entry], isodate)
            case 'sun':
                return await sun.generate_states(self.schedule_entry[schedule_entry], isodate)
            case 'time':
                return await time.generate_states(self.schedule_entry[schedule_entry], isodate)
            case None:
                raise Exception('MissingEntryInSchedule')
            case _:
                raise Exception('UnknownEntryInSchedule', schedule_entry)
