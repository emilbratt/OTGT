from . import elspot, sun, time


class Schedule:

    def __init__(self, schedule_entry: dict):
        self.schedule_entry = schedule_entry

    async def generate_states(self, isodate: str):
        schedule_entry = None
        for entry in self.schedule_entry:
            if self.schedule_entry[entry]['include_entry']:
                schedule_entry = entry
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
