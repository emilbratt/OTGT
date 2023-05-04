from cocuvida.timehandle import isodates


class Calendar:
    def __init__(self, calendar_entry: dict):
        self.calendar_entry = calendar_entry

    async def is_excluded_date(self, isodate: str) -> bool:
        if self.calendar_entry['exclude_dates']['include_entry']:
            for v in self.calendar_entry['exclude_dates']['entries']:
                cp_date = v
                if v.startswith('--'):
                    cp_date = isodates.add_this_year_to_isodate(v)
                if isodate == cp_date:
                    return True
        return False

    async def is_included_date(self, isodate: str) -> bool:
        if self.calendar_entry['include_dates']['include_entry']:
            for v in self.calendar_entry['include_dates']['entries']:
                cp_date = v
                if v.startswith('--'):
                    cp_date = isodates.add_this_year_to_isodate(v)
                if isodate == cp_date:
                    return True
        return False

    async def is_included_weekday(self, isodate: str) -> bool:
        weekday = isodates.weekday_name_from_isodate(isodate)
        if self.calendar_entry['weekdays']['include_entry']:
            if self.calendar_entry['weekdays'][weekday.lower()]:
                return True
        return False

    async def date_is_included_holiday(calendar: dict, isodate: str) -> str:
        # FIXME: IMPLEMENT HOLIDAY ENTRY
        raise Exception('MethodNotImplemented')