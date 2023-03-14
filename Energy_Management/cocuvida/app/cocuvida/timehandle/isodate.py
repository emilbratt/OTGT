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

def timestamp_now() -> str:
    '''
        returns datetime as iso format down to seconds e.g. '2023-01-22T15:37:13'
    '''
    return datetime.now().isoformat(timespec='seconds')

def weekday() -> int:
    '''
        returns weekday as int | monday=1 | sunday=7
    '''
    return datetime.now().isoweekday()
