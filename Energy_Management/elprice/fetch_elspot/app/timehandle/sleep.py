from time import sleep
from datetime import datetime

def seconds(seconds: int=1):
    '''
        sleep for x seconds
    '''
    sleep(seconds)

def until_next_hour() -> int:
    '''
        pause script until next full hour
        e.g. if time is 14:25 then sleep for 35 minutes -> 15:00

        returns the current hour as int 0-23
    '''
    minutes_until_new_hour = 60 - datetime.now().minute
    sleep_seconds = minutes_until_new_hour * 60
    sleep(sleep_seconds)
    return datetime.now().hour


def until_next_half_hour() -> int:
    '''
        pause script until next half hour (13:00, 13:30, 14:00, 14:30 e.g.)
        e.g. if time is 14:05 then sleep for 25 minutes -> 14:30

        returns the current minute as int 0-59
    '''
    current_minute = datetime.now().minute
    substract_minutes = 30 * (1 + (current_minute >= 30))
    minutes_left = substract_minutes - current_minute
    minutes_to_seconds = 60 * minutes_left
    seconds_left = minutes_to_seconds - datetime.now().second
    sleep(seconds_left)
    return datetime.now().minute


def until_next_quarter_hour() -> int:
    '''
        pause script until next full quarter (13:00, 13:15, 13:30, 13,45 e.g.)
        e.g. if time is 14:05 then sleep for 10 minutes -> 14:15

        returns the current minute as int 0-59
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
    seconds_left = minutes_to_seconds - datetime.now().second
    sleep(seconds_left)
    return datetime.now().minute


def until_next_minute() -> int:
    '''
        pause script until next full minute
        e.g. if time is 14:05:45 then sleep for 15 seconds -> 14:06

        returns the current minute as int 0-59
    '''
    sleep(60 - datetime.now().second)
    return datetime.now().minute


def until_time_of_day(hour: int, minute: int) -> tuple:
    '''
        sleep until a specified time (24h format)
        first param = hour, second param = minutes
        returns current time as int stored in a tuple (hour, minute)
    '''
    # convert to total seconds passed for this day
    t = datetime.now()
    seconds_now = (t.now().hour*3600) + (t.now().minute*60) + (t.now().second)
    seconds_target = (hour*3600) + (minute*60)
    is_next_day = (seconds_now > seconds_target)
    sleep_seconds = (is_next_day * 86400) + seconds_target - seconds_now
    sleep(sleep_seconds)
    return (datetime.now().hour, datetime.now().minute)
