#!/usr/bin/env python3

from time import sleep

import LEDReporter
import Database
import UserInput
try:
    from gpiozero import LED,PWMLED
    ledreport = LED(17)
except ModuleNotFoundError:
    ledreport = False
    print('gpiozero not found, disabling LED')

def insert_jobs(userinput):
    print('insert_jobs()')
    for job in userinput.jobs:
        Database.InsertJob(job)
    userinput.reset()
    LEDReporter.ScanItem(ledreport)

def mainloop():
    userinput = UserInput.UserInput()
    LEDReporter.ScanItem(ledreport) # default on first round, indicate item scan ready
    while True:
        print('userinput.get()')
        userinput.get()
        item_count = len(userinput.items)
        if item_count == 1: # on first valid item scan, indicate shelf scan ready
            LEDReporter.ScanShelf(ledreport)
        elif item_count > 1: # on 2nd++ item scan, indicate multiple item scan ready
            LEDReporter.ScanMultipleItems(ledreport)

        if userinput.type == 'shelf':
            insert_jobs(userinput)

def init():
    Database.StartDatabase()
    data = {
        'item': '3847261526364',
        'shelf': 'A-A-1',
        'status': '0',
    }

    Database.InsertJob(data)



if __name__ == '__main__':
    init()
    mainloop()
