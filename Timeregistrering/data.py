#!/usr/bin/env python3
from time import sleep
from datetime import datetime
import os
import json
from log import Log


timeStampBegin = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")[:-4]
startDate = datetime.now().strftime("%Y-%m-%d")
mainPath = os.path.dirname(os.path.realpath(__file__))
dataPath = os.path.join(mainPath, "data")
usersJson = os.path.join(mainPath, "data", "users.json")


# create new users.json if none
if os.path.isfile(usersJson) == False:
    with open(usersJson, 'a') as newJsonFile:
        newJsonFile.write("{}")


class Data:
    def __init__(self):
        os.makedirs(dataPath, exist_ok=True)
        # load users
        with open(usersJson,encoding='UTF-8') as jsonFile:
            self.users = json.load(jsonFile)

        self.datalog = Log()



    def add(self, user):
        self.userLog = Log(user)
        try:
            json_file = open(usersJson,encoding='utf-8')
            try:
                self.users = json.load(json_file)
            except json.decoder.JSONDecodeError:
                self.userLog.add('json.decoder.JSONDecodeError on ./data/users.json')


            json_file.close()
        except FileNotFoundError:
            self.log = {self.ID:{
                timeStampBegin:'FileNotFoundError, new file created'}
            }


if __name__ == '__main__':
    kake = Log('emil')
    kake.add('json.decoder.JSONDecodeError on ./data/users.json')
