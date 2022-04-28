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
    for job in userinput.jobs:
        Database.InsertJob(job)
    userinput.reset()
    LEDReporter.ScanItem(ledreport)

def mainloop():
    Database.StartDatabase() # will force create db and table if not exists
    userinput = UserInput.UserInput() # this handles input of item and shelf values
    LEDReporter.ScanItem(ledreport) # default on first round, indicate item scan ready
    while True:
        print('userinput.get()')
        userinput.get()
        if userinput.type == 'shelf':
            print('insert_jobs()')
            insert_jobs(userinput)

        item_count = len(userinput.items)
        if item_count == 1: # on first valid item scan, indicate shelf scan ready
            LEDReporter.ScanShelf(ledreport)
        elif item_count > 1: # on 2nd++ item scan, indicate multiple item scan ready
            LEDReporter.ScanMultipleItems(ledreport)



if __name__ == '__main__':
    mainloop()
