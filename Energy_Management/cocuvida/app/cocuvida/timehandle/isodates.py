from datetime import datetime, timedelta


def today() -> str:
    '''
        returns datetime as iso format e.g. '2023-01-22'
    '''
    return datetime.now().strftime('%Y-%m-%d')

def today_plus_days(days: int) -> str:
    '''
        param:
            days = how many days to add (can be negative)
        returns
            datetime as iso format e.g. '2023-01-22'
    '''
    delta_time = datetime.now() + timedelta(days=days)
    return delta_time.strftime('%Y-%m-%d')

def timestamp_now() -> str:
    '''
        returns datetime as iso format down to seconds e.g. '2023-01-22 15:37:13'
    '''
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def timestamp_now_round(unit: str) -> str:
    '''
        returns datetime as iso format  '2023-01-22 15:37:13'
        takes input as second, minute or hour
    '''
    match unit:
        case 'second':
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        case 'minute':
            return datetime.now().strftime('%Y-%m-%d %H:%M')
        case 'hour':
            return datetime.now().strftime('%Y-%m-%d %H') 
        case _:
            raise Exception(f'InvalidTimeUnit: {unit}')

def weekday_number_today() -> int:
    '''
        returns weekday as int | monday=1 | sunday=7
    '''
    return datetime.now().isoweekday()

def weekday_name_today() -> str:
    '''
        returns weekday as string e.g. monday or tuesday
    '''
    return datetime.now().strftime('%A')

def weekday_name_from_isodate(isodate: str) -> str:
    '''
        pass dates as
            '--MM-DD' -> date for every year (will use current year)
            'YYYY-MM-DD' -> date for specific year
        returns weekday as string e.g. Monday or Tuesday
        
    '''
    if isodate.startswith('--'):
        isodate = isodate.strip('--')
        isodate = str(datetime.now().year) + '-' + isodate
    return datetime.fromisoformat(isodate).strftime('%A')

def add_this_year_to_isodate(isodate: str) -> str:
    '''
        pass dates as '--MM-DD' -> returns 'YYYY-MM-DD' with this years YYY
    '''
    isodate = isodate.strip('--')
    return str(datetime.now().year) + '-' + isodate

def get_holiday_name(isodate: str) -> bool:
    '''
        pass dates as
            '--MM-DD' -> date for every year
            'YYYY-MM-DD' -> date for specific year
        returns name of holiday if found, else returns False
    '''
    raise Exception('NotImplementedYet')

def date_object_from_isodate(isodate: str) -> datetime:
    '''
        pass timestamp as
            '--MM-DD' -> date for every year
            'YYYY-MM-DD' -> date for specific year
    '''
    if isodate.startswith('--'):
        isodate = isodate.strip('--')
        isodate = str(datetime.now().year) + '-' + isodate
        return datetime.fromisoformat(isodate)
    return datetime.fromisoformat(isodate)

def date_object_from_timestamp(timestamp: str) -> datetime:
    '''
        pass isotimestamp as 'YYYY-MM-DD HH:MM:SS'
                          or 'YYYY-MM-DDTHH:MM:SS'
    '''
    return datetime.fromisoformat(timestamp)

def date_from_timestamp(timestamp: str) -> str:
    '''
        pass isotimestamp as 'YYYY-MM-DD HH:MM:SS'
                          or 'YYYY-MM-DDTHH:MM:SS'
        returns 'YYYY-MM-DD'
    '''
    date_obj = datetime.fromisoformat(timestamp)
    return date_obj.strftime('%Y-%m-%d')

def time_from_timestamp(timestamp: str) -> str:
    '''
        pass isotimestamp as 'YYYY-MM-DD HH:MM:SS'
                          or 'YYYY-MM-DDTHH:MM:SS'
        returns 'HH:MM:SS'
    '''
    date_obj = datetime.fromisoformat(timestamp)
    return date_obj.strftime('%H:%M:%S')

def add_minutes_to_timestamp(timestamp: str, minutes: int):
    '''
      pass timestamp as 'YYYY-MM-DD HH:MM:SS' and minutes as int
      returns same timestamp format, but with adjusted minutes
    '''
    date_obj = datetime.fromisoformat(timestamp)
    date_obj = date_obj + timedelta(minutes=minutes)
    return date_obj.strftime('%Y-%m-%d %H:%M:%S')
