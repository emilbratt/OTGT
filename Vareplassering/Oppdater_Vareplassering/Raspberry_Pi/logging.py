#!/usr/bin/env python3
from time import sleep
from datetime import datetime
import os
import json
logLevel = ["\033[92m","\033[91m","\033[93m","\033[96m","\033[95m","\033[94m"]
startTime = datetime.now().strftime("%H:%M:%S")


class Log:
    '''
        syntax: Log('message', option)

        options:
        1-5 (colours representing the warning level)
        noprint (only store log, dont print it on screen)

        example:
        Log('task completed', 0)
        example 2:
        Log('could not find json file', 1)
        example 3:
        Log('password = variable', 'noprint')
    '''
    def __init__(self, data, type='0'):
        sleep(0.01)
        os.makedirs('%s/log'%os.path.dirname(os.path.realpath(__file__)), exist_ok=True)
        self.getTime = datetime.now()
        self.startTime = startTime
        self.fileName = self.getTime.strftime("%Y-%m-%d")
        self.clock = self.getTime.strftime("%H:%M:%S.%f")[:-4]
        self.file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log', self.fileName)
        self.type = type
        self.logLevel = logLevel

        # load json, convert to dict, add log to dict, save dict to json
        try:
            json_file = open('%s.json'%self.file,encoding='utf-8')
            try:
                self.log = json.load(json_file)
            except json.decoder.JSONDecodeError:
                self.log = {self.startTime:{self.clock:'JSONDecodeError on log, creating new'}}
                print('JSONDecodeError on log, creating new')

            json_file.close()
        except FileNotFoundError:
            print('\t\033[93mlog file not found, creating new\033[0m')
            self.log = {self.startTime:{self.clock:'log file not found, creating new'}}


        if self.type == 'noprint':
            pass
        else:
            print(f'\t{self.logLevel[int(self.type)]}{data}\033[0m')

        try:
            self.log[self.startTime].update({self.clock:data})
        except KeyError: # will create a new key (usually at first appended log)
            self.log[self.startTime] = {self.clock:data}

        json_file = open('%s.json'%self.file, 'w',encoding='utf-8')
        json.dump(self.log, json_file, indent=2)
        json_file.close()
