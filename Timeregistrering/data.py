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
dataJson = os.path.join(mainPath, "data", "db.json")


# create new db.json if none
if os.path.isfile(dataJson) == False:
    with open(dataJson, 'a') as newJsonFile:
        newJsonFile.write("{}")

# write changes to database
def updateDB(db):
    with open(dataJson, 'w',encoding='utf-8') as loadFile:
        json.dump(db, loadFile, indent=2)
    # loadFile.close()

class Database:
    def __init__(self,user='main'):
        # if no datadir, create
        os.makedirs(dataPath, exist_ok=True)

        # load db
        with open(dataJson,encoding='UTF-8') as jsonFile:
            self.db = json.load(jsonFile)

        self.dataLog = Log(user)

        try:
            loadFile = open(dataJson,encoding='utf-8')
            try:
                self.db = json.load(loadFile)
            except json.decoder.JSONDecodeError:
                self.dataLog.add('json.decoder.JSONDecodeError'+
                    'on ./data/db.json, new file created')


            loadFile.close()
        except FileNotFoundError:
            self.dataLog.add('FileNotFoundError on ./data/db.json, '+
                'new file created')
            self.db = {self.ID:{
                timeStampBegin:'FileNotFoundError, new file created'}
            }


    def showUsers(self):
        print('\t    Alle Navn:')
        for key in self.db:
            print(f'\t\tBruker ID: {key} {self.db[key]["user"]}')



    def addWork(self):
        pass

    def addUser(self, name):
        print(type(str(int(max(self.db)))))
        for value in self.db.values():
            if name in value['user']:
                print(f'\tBrukernavn {name} eksisterer allerede')
                return None
        self.dataLog.add(f'Added user {name}')
        self.db.setdefault(str(int(max(self.db))+1),{'user':name})
        # self.db.setdefault(len(self.db)+1,{'user':name})
        print(f'\tBrukernavn {name} ble lagt til med ID nr {max(self.db)} ')
        updateDB(self.db)

    # def removeUser()

# example usage
if __name__ == '__main__':
    db = Database()
    db.addUser('mike')
    db.showUsers()
    exit()
