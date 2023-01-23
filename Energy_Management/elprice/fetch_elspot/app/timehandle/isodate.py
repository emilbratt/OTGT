from datetime import datetime, timedelta

def today() -> str:
    '''
        returns datetime as iso format e.g. '2023-01-22'
    '''
    return datetime.today().strftime('%Y-%m-%d')

def today_plus_days(days: int) -> str:
    '''
        param:
            days = how many days to add (can be negative)
        returns
            datetime as iso format e.g. '2023-01-22'
    '''
    val = datetime.today() + timedelta(days=days)
    return val.strftime('%Y-%m-%d')


def today_seconds() -> str:
    '''
        returns datetime as iso format down to seconds e.g. '2023-01-22T15:37:13'
    '''
    return datetime.now().isoformat(timespec='seconds')


def today_minutes() -> str:
    '''
        returns datetime as iso format down to minutes e.g. '2023-01-22T15:37'
    '''
    return datetime.now().isoformat(timespec='minutes')


def today_hours() -> str:
    '''
        returns datetime as iso format down to hours e.g. '2023-01-22T15'
    '''
    return datetime.now().isoformat(timespec='hours')


def convert_to_seconds(year: int, month: int, day: int, hour: int, minute: int, second: int) -> str:
    '''
        exapmle.
        call:
            isodate.convert_to_iso(2021, 10, 24, 8, 48, 23)
        returns
            '2021-10-24T08:48:23'
    '''
    org = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
    return org.isoformat(timespec='seconds')


def convert_to_minutes(year: int, month: int, day: int, hour: int, minute: int) -> str:
    '''
        exapmle.
        call:
            isodate.convert_to_iso(2021, 10, 24, 8, 48)
        returns
            '2021-10-24T08:48'
    '''
    org = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    return org.isoformat(timespec='minutes')


def convert_to_hours(year: int, month: int, day: int, hour: int) -> str:
    '''
        exapmle.
        call:
            isodate.convert_to_iso(2021, 10, 24, 8)
        returns
            '2021-10-24T08'
    '''
    org = datetime(year=year, month=month, day=day, hour=hour)
    return org.isoformat(timespec='hours')
