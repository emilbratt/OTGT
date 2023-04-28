from datetime import datetime


def until_next_minute() -> int:
    '''
        return seconds until next full minute
        e.g. if time is 14:05:45 then return 15
    '''
    return (60 - datetime.now().second)

def until_next_quarter_hour() -> int:
    '''
        return seconds until next full quarter (13:00, 13:15, 13:30, 13,45 e.g.)
    '''
    current_minute = datetime.now().minute
    current_quarter = current_minute - (current_minute % 15)
    match current_quarter:
        case 0: # wait until xx:15
            minutes_left = 15 - current_minute
        case 15: # wait until xx:30
            minutes_left = 30 - current_minute
        case 30: # wait until xx:45
            minutes_left = 45 - current_minute
        case 45: # wait until xx:00
            minutes_left = 60 - current_minute

    minutes_to_seconds = 60 * minutes_left
    return minutes_to_seconds - datetime.now().second

def until_next_half_hour() -> int:
    '''
        return seconds until next half hour (13:00, 13:30, 14:00, 14:30 e.g.)
    '''
    current_minute = datetime.now().minute
    substract_minutes = 30 * (1 + (current_minute >= 30))
    minutes_left = substract_minutes - current_minute
    minutes_to_seconds = 60 * minutes_left
    return minutes_to_seconds - datetime.now().second

def until_next_hour() -> int:
    '''
        return seconds until next full hour
    '''
    minutes_until_new_hour = 60 - datetime.now().minute
    return minutes_until_new_hour * 60

def until_time_of_day(timeofday: str) -> int:
    '''
        pass string in format 'HH:MM'

        returns seconds until specified time of day (24h format)
    '''
    isodate = datetime.now().strftime('%Y-%m-%d')
    f = datetime.fromisoformat(f'{isodate} {timeofday}')
    t = datetime.now()
    return (f - t).seconds

def until_timestamp(timestamp: str) -> int:
    '''
        pass string in format 'YYYY-MM-DD HH:MM'

        returns seconds until specified timestamp
    '''
    f = datetime.fromisoformat(timestamp)
    t = datetime.now()
    return (f - t).seconds

def between_timestamps(timestamp_1: str, timestamp_2: str) -> int:
    '''
        returns seconds between two iso timestamps
        pass timestamps as 'YYYY-MM-DD HH:MM:SS'
    '''
    f = datetime.fromisoformat(timestamp_1)
    g = datetime.fromisoformat(timestamp_2)
    if f < g:
        return int((g - f).total_seconds())
    else:
        return int((f - g).total_seconds())
