from datetime import datetime


def now() -> str:
    '''
      returns 24 hour format -> 'HH:MM:SS'
    '''
    return datetime.now().strftime('%H:%M:%S')

def now_quarterhour() -> str:
    '''
      returns 24 hour format -> 'HH:MM' for the last passed quarter hour
      if time is 13:32, return 13:30
    '''
    time_now = datetime.now()
    minute = time_now.minute
    if minute < 15:
        minute = 0
    elif minute < 30:
        minute = 15
    elif minute < 45:
        minute = 30
    else:
        minute = 45
    time_now = time_now.replace(minute=minute)
    return time_now.strftime('%H:%M')

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
    time_now = datetime.now()
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    subtracted = time_now - start_of_day
    return subtracted.total_seconds()


# FIXME: change parameter for the two functions below (instead of taking two INtime_now, take a str with "HH:MM")
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
