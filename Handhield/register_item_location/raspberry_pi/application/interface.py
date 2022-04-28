#!/usr/bin/env python3

from time import sleep

import Database
import UserInput


def insert_jobs(userinput):
    print('insert_jobs()')
    for job in userinput.jobs:
        Database.InsertJob(job)
    userinput.reset()

def mainloop():
    userinput = UserInput.UserInput()
    while True:
        print('userinput.get()')
        userinput.get()
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
