#!/usr/bin/env python3
from time import sleep
from datetime import datetime
import os
import json

# declare time, date and path
# timeStart = datetime.now().strftime("%H:%M:%S")
# startTime = datetime.now().strftime("%H:%M:%S")
timeStampBegin = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")[:-4]
startDate = datetime.now().strftime("%Y-%m-%d")
logPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "log")


class Log:
    def __init__(self,user='main'):
        # if no logdir, create
        os.makedirs(logPath, exist_ok=True)

        # declare first key in json depending on main or a username
        if user != 'main':
            self.filePath = os.path.join(logPath, 'users.json')
            self.ID = user
        else:
            self.filePath = os.path.join(logPath, 'main.json')
            self.ID = datetime.now().strftime("%Y-%m-%d")


        # self.timeStamp = datetime.now().strftime(
        #     "%H:%M:%S.%f")[:-4]

        # initialize json file
        try:
            json_file = open(self.filePath,encoding='utf-8')
            try:
                self.log = json.load(json_file)
            except json.decoder.JSONDecodeError:
                    self.log = {self.ID:{
                    timeStampBegin:'json.decoder.JSONDecodeError, new file created'
                    }
                }

            json_file.close()
        except FileNotFoundError:
            self.log = {self.ID:{
                timeStampBegin:'FileNotFoundError, new file created'}
            }

        # force a micro delay to avoid timestamp duplicate
        sleep(0.02)
        try:
            self.log[self.ID].update({datetime.now().strftime(
                "%Y-%m-%d_%H:%M:%S.%f")[:-4]:'Start'})
        except KeyError: # will create a new key (usually at first appended log)
            self.log[self.ID] = {datetime.now().strftime(
                "%Y-%m-%d_%H:%M:%S.%f")[:-4]:'Start'}
        sleep(0.02)


    def add(self, data):

        # force a micro delay to avoid timestamp duplicate
        sleep(0.02)
        self.timeStamp = datetime.now().strftime(
            "%Y-%m-%d_%H:%M:%S.%f")[:-4]

        try:
            self.log[self.ID].update({self.timeStamp:data})
        except KeyError: # will create a new key (usually at first appended log)
            self.log[self.ID] = {self.timeStamp:data}


        json_file = open(self.filePath, 'w',encoding='utf-8')
        json.dump(self.log, json_file, indent=2)
        json_file.close()


# example usage
if __name__ == '__main__':
    mainLog = Log()
    mainLog.add('Log that goes into main.json')

    userLog = Log('Jack')
    userLog.add('Log that goes into user Jack in users.json')
