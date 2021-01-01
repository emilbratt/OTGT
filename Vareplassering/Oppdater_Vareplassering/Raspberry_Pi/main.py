#!/usr/bin/env python3
__author__ = "Emil Bratt Børsting"
__email__  = "emilbratt@gmail.com"
__status__ = "production"

# use this as a template for your own projects
# you will have to modify it to fit your purpose
from time import sleep
# sleep is used mainly to distinguish logs which are timestamped
# by forcing a .1 second delay between each record
# i will probably rewrite how this is handled (maybe use it in the logging.py file)
import socket # for getting hostname and ip address
import csv
import sys # handles arguments (flags) when running the file
from datetime import datetime
import os
import json

# local modules
from inventory import Inventory
from writelog import Log

# optionally add flags
'''
    run with "./main.py <name>"  (where name is the mode/flag)
    you can add more flags after each other ./main.py <flag1> <flag2> etc..

    mode
        will not run the program but instead check what
        is enabled/disabled in debug.json and print on screen

        when running on pi in normal enviroment, set all to True
        when debugging set needed values to false

        how: by adding one or more flags as shown under
        example: switch shutdown and sql -> python3 main.py shutdown sql

    passwordhide
        enable/disable passwrod printing on screen

    shutdown
        enable/disable shutdown on error

    sql
        enables/disables sql updating

    led
        enables/disables the gpio led

    credentials
        add new credentials settings

    wipesessions
        removes all csv files in ./inventory/sessions

    build
        builds a json file with all barcodes and shelves from session files

    live
        set live mode (keep running after update)

    showcred
        enable/disable displaying server, port, database and user on screen
'''


absPath = os.path.dirname(os.path.realpath(__file__))
os.makedirs('%s/log' % absPath, exist_ok=True)
os.makedirs('%s/inventory' % absPath, exist_ok=True)
os.makedirs('%s/inventory/sessions' % absPath, exist_ok=True)

def checkDate():
    '''
        we store new values in a sesssion file

        each session file represents a fixed date so that it is
        easy to keep track of the new values added

        this function returns true if the time stamp
        is greater than the latest session file

        this is important because we incrementally add new
        session files for each date moving forward

        with values being added every now and then we do not want to iterate
        through an ever growing list of values when updating shelf values,
        but rather only from the newest session file
    '''

    # if no files are present for date verification then
    # set prefixed date so we have something to use as a filename - see except ValueError
    getcsvDates = [file for file
    in os.listdir('%s/inventory/sessions'%
    os.path.dirname(os.path.realpath(__file__)))
    if os.path.splitext(file)[-1] == '.csv']
    try:
        fromcsv = int(max(getcsvDates).replace('.csv', ''))
    except ValueError:
        fromcsv = 20200101

    for i in range(5):
        fromdatetime = int(datetime.now().strftime("%Y%m%d"))
        if fromdatetime < fromcsv:
            if i == 4:
                return False
            sleep(3)
            return True
        else:
            return True


def getIP():
    '''
        returns the ip address of the device
    '''
    interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        interface.connect(('10.255.255.255', 1))
        IP = interface.getsockname()[0]
    except Exception:
        IP = 'connection_error'
    finally:
        interface.close()
    return IP


def ledBlink(value):
    '''
        this function handles the LED that is connected to the GPIO board

        plug the + wire of the led into gpio pin number 11 (tested on raspberry pi 3B)
    '''
    if debug['led'] == False:
        return None
    if value == 'item':
        led.off()
        led.value = 0.5  # half brightness
        led.blink(0.2,0.5)
    elif value == 'shelf':
        led.off()
        led.value = 0.5
        led.blink(0.05,0.2)
    elif value == 'invalid':
        led.off()
        led.value = 1
        led.blink(0.02,0.06)
    elif value == 'update':
        led.off()
        led.value = 1 # full brightness
        led.blink(2,1.5)
    return None

def mainLoop():
    '''
        this function will loop while you add items and shelf values

        it will end (and restart if debug.json is set with the live parameter = true)
        when you scan the excUpdate barcode that is located in the ekstra directory
    '''
    # initialize inventory
    inventory = Inventory()

    # start scanning barcodes from items and shelves
    while True:
        ledBlink('item')
        item = input('\n\t\033[96mscan item: ')
        if item.isnumeric():
            ledBlink('shelf')
            shelf = input('\n\tscan shelf: ')
            if '-'  in shelf:
                inventory.sessionAdd(item,shelf)
                continue
            else:
                if shelf == 'excUpdate':
                    ledBlink('update')
                    inventory.sessionExecuteUpdate()
                    del inventory
                    return True
                elif shelf == 'exit':
                    return False
                else:
                    Log(shelf + ' is not a valid shelf barcode',2)
                    sleep(0.5)
        else:
            if item == 'excUpdate':
                ledBlink('update')
                inventory.sessionExecuteUpdate()
                del inventory
                return True
            elif item == 'exit':
                return False
            else:
                Log(item + ' is not a valid item barcode',2)
                sleep(0.5)
                continue




if __name__ == '__main__':
    validFlags = [
        'mode','passwordhide', 'build',
        'shutdown','sql','led',
        'credentials','wipesessions','live',
        'showcred'
        ]
    # put file directory into a variable
    cwd = os.path.dirname(os.path.realpath(__file__))

    # check for correct date before initializing
    dateOK = checkDate()
    if dateOK == True:
        pass

        '''do something'''
    else:
        '''do something else'''
        Log('Could not load the correct date, '
        + 'creating a temp session for this instance', 1)


    Log(f'executing {__file__}','5')


    # open debug and check parameters
    mode = open('%s/debug.json'%cwd,encoding='utf-8')
    debug = json.load(mode)
    mode.close()
    # check modes in debug.json
    if 'mode' in sys.argv:
        for key in debug:
            print(f'{key} = {debug[key]}')

    # apply all arguments
    for i in range(1,len(sys.argv)):
        try:
            if debug[sys.argv[i]] == True:
                debug[sys.argv[i]] = False
                Log(f'Deactivating {sys.argv[i]}', 4)
            else:
                debug[sys.argv[i]] = True
                Log(f'Activating {sys.argv[i]}', 3)
        except KeyError:
            if sys.argv[i] == 'wipesessions':
                Log(f'executing {__file__} with wipesessions flag')
                Inventory().wipeSessions()
            elif sys.argv[i] == 'credentials':
                Log(f'executing {__file__} with credentials flag')
                from credentials import createCredentials
                createCredentials()
            elif sys.argv[i] == 'build':
                from databuild import Build
                Log(f'executing {__file__} with build flag')
                dataFile = Build()
                dataFile.runbuild()
            else:
                Log(f'executing {__file__} with {sys.argv[i]} flag')
                Log(f'{sys.argv[i]} is an invalid flag')
                print('\tvalid flags:')
                for flag in validFlags:
                    print('\t\t./main.py '+flag)

        with open('%s/debug.json'%cwd, 'w',encoding='utf-8') as mode:
            json.dump(debug, mode, indent=2)
    # exit if any arguments where given
    if len(sys.argv) > 1:
        exit()




    debugMode = False
    # warn user if any parameter is disabled
    for key in debug:
        if debug[key] == False:
            Log(f'{key} is deactivated', 2)
            debugMode = True
        sleep(0.5)

    if debugMode == True:
        Log('running in debug mode', 3)
    # import shutdown
    if debug['shutdown'] == True:
        from subprocess import call

    # import LED
    if debug['led'] == True:
        try:
            # import gpiozero module only if led is not disabled in debug.json
            from gpiozero import LED,PWMLED
            led = LED(17)
        except ModuleNotFoundError:
            try:
                call("echo", shell=True)
                Log('gpiozero module was not found, shutting down', 1)
                sleep(2)
                call("sudo nohup shutdown -h now", shell=True)
            except NameError:
                Log('gpiozero module was not found, exiting', 1)
                sleep(2)
                exit()

    # only continue if connected to network
    for i in range(5):
        if getIP() == 'connection_error':
            sleep(3)
            if i == 4:
                Log(getIP(),1)
                try:
                    call("echo", shell=True)
                    Log('no network connection found, shutting down', 1)
                    sleep(2)
                    call("sudo nohup shutdown -h now", shell=True)
                except NameError:
                    Log('no network connection found, exiting', 1)
                    sleep(2)
                    exit()
        else:
            Log(f'ip address: {getIP()}')
            break

    # start
    Log(f'hostname: {socket.gethostname()}')
    Log(f'full path: {cwd}', 'noprint')

    # run the application
    while True:
        if mainLoop() == False:
            exit()
