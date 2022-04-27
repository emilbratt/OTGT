#!/usr/bin/env python3

from time import sleep

try:
    from gpiozero import LED,PWMLED
    ledreport = LED(17)
except ModuleNotFoundError:
    ledreport = False
    print('gpiozero not found, disabling LED')

import Database
import LEDReporter
import UserInput


def mainloop():
    userinput = UserInput.UserInput()
    while True:
        LEDReporter.ScanItem(ledreport)
        sleep(2)
        LEDReporter.ScanShelf(ledreport)
        sleep(2)
        LEDReporter.ScanMultipleItems(ledreport)
        sleep(2)
        userinput.item()
        print(userinput.value)
        print(userinput.type)
        userinput.shelf()
        print(userinput.value)
        print(userinput.type)
        exit()


def init():
    Database.StartDatabase()
    data = {
        'barcode': '3847261526364',
        'shelf': 'A-A-1',
        'status': '0',
    }

    Database.InsertJob(data)



if __name__ == '__main__':
    init()
    mainloop()
