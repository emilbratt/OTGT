#!/usr/bin/env python3

import Database
import LEDReporter


def mainloop():
    while True:
        exit()

def init():
    Database.StartDatabase()
    data = {
        'barcode': '3847261526364',
        'shelf': 'A-A-1',
        'status': '0',
    }

    Database.InsertJob(data)
    LEDReporter.ScanItem(17)


if __name__ == '__main__':
    init()
    mainloop()
