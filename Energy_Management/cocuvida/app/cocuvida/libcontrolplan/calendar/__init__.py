from cocuvida.timehandle import isodates


class Calendar:
    def __init__(self, calendar_entry: dict):
        self.calendar_entry = calendar_entry

    async def is_excluded_date(self, isodate: str) -> bool:
        if 'exclude_dates' not in self.calendar_entry:
            return False
        elif not self.calendar_entry['exclude_dates']['include_entry']:
            return False
        for v in self.calendar_entry['exclude_dates']['entries']:
            cp_date = v
            if v.startswith('--'):
                cp_date = isodates.add_this_year_to_isodate(v)
            if isodate == cp_date:
                return True
        return False

    async def is_included_date(self, isodate: str) -> bool:
        if 'include_dates' not in self.calendar_entry:
            return False
        elif not self.calendar_entry['include_dates']['include_entry']:
            return False
        for v in self.calendar_entry['include_dates']['entries']:
            cp_date = v
            if v.startswith('--'):
                cp_date = isodates.add_this_year_to_isodate(v)
            if isodate == cp_date:
                return True
        return False

    async def is_excluded_weekday(self, weekday: str) -> bool:
        if 'exlude_weekdays' not in self.calendar_entry:
            return False
        elif not self.calendar_entry['exlude_weekdays']['include_entry']:
            return False
        weekday = weekday.lower()
        for day in self.calendar_entry['exlude_weekdays']['entries']:
            if weekday == day:
                return True
        return False

    async def is_included_weekday(self, weekday: str) -> bool:
        if 'include_weekdays' not in self.calendar_entry:
            return False
        if not self.calendar_entry['include_weekdays']['include_entry']:
            return False
        weekday = weekday.lower()
        for day in self.calendar_entry['include_weekdays']['entries']:
            if day.lower() == weekday:
                return True
        return False

    async def date_is_included_holiday(calendar: dict, isodate: str) -> str:
        # FIXME: IMPLEMENT HOLIDAY ENTRY
        raise Exception('MethodNotImplemented')