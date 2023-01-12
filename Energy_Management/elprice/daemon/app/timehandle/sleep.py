from time import sleep
from datetime import datetime

def until_next_hour() -> int:
    '''
        this function will pause script until the next full hour reached
        e.g. if time is 14:25, this function will sleep for 35 minutes
        until time is 15:00
    '''


    while True:
        minutes_until_new_hour = 60 - datetime.now().minute
        sleep_seconds = minutes_until_new_hour * 60
        sleep(sleep_seconds)
        return datetime.now().hour
