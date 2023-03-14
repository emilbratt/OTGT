from datetime import datetime


def now() -> str:
    '''
      returns 24 hour format -> 'HH:MM'
    '''
    h = datetime.now().hour
    m = datetime.now().minute
    return str(h).zfill(2) + ':' + str(m).zfill(2)

def hour() -> int:
    '''
      returns 24 hour format as int
    '''
    return datetime.now().hour

def minute() -> int:
    '''
      returns minutes as int
    '''
    return datetime.now().minute

def second() -> int:
    '''
      returns seconds as int
    '''
    return datetime.now().second

def total_seconds_elapsed_today() -> int:
    return (datetime.now().hour*3600) + (datetime.now().minute*60) + (datetime.now().second)

def is_passed_time(hour: int, minute: int) -> bool:
    '''
      pass hour (0-23) and minute (0-59)
      returns True if current time of day is passed, False if not
    '''
    if datetime.now().hour > hour:
        return True
    if datetime.now().hour == hour and datetime.now().minute >= minute:
        return True
    return False

def is_before_time(hour: int, minute: int) -> bool:
    '''
      pass hour (0-23) and minute (0-59)
      returns True if current time of day is before, False if not
    '''
    if datetime.now().hour < hour:
        return True
    if datetime.now().hour == hour and datetime.now().minute < minute:
        return True
    return False
