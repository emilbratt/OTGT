#!/usr/bin/env python3

import Database
import LEDReporter
from time import sleep

ledreport = False
try:
    from gpiozero import LED,PWMLED
    ledreport = LED(17)
except ModuleNotFoundError:
    print('gpiozero not found, disabling LED')


def mainloop():

    while True:
        LEDReporter.ScanItem(ledreport)
        sleep(4)
        LEDReporter.ScanShelf(ledreport)
        sleep(4)
        LEDReporter.ScanMultipleItems(ledreport)
        sleep(4)
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
