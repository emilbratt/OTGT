import json
import csv
import os
from time import sleep
from logging import Log

class Build:
    def __init__(self):

        self.inventoryPath = os.path.join(
        os.path.dirname(os.path.realpath(
        __file__)), 'inventory')

        self.dataPath = os.path.join(
        os.path.dirname(os.path.realpath(
        __file__)), 'inventory', 'data.json')


        self.sessionPath = os.path.join(
        os.path.dirname(os.path.realpath(
        __file__)), 'inventory/sessions')

        self.data = {}


    # build inventory for items and shelf value
    def runbuild(self):
        sessions = []
        for fileName in os.listdir(self.sessionPath):
            if os.path.splitext(fileName)[-1] == '.csv':
                Log(f'Building data.json from {fileName} ')
                sessions.append(int(fileName[:-4]))

        for file in sessions:
            sessionFile = os.path.join(self.sessionPath,str(file))

            with open('%s.csv' % sessionFile,'r') as csvfile:
                reader = csv.reader(csvfile)

                for row in reader:
                    item = row[0]
                    shelf = row[1]

                    if item not in self.data:
                        self.data.setdefault(item, [])

                    self.data.setdefault(item, []).append(shelf)

        with open(self.dataPath, 'w',encoding='utf-8') as jsonLoad:
            Log('Saving data.json')
            json.dump(self.data, jsonLoad, indent=2)


if __name__ == '__main__':
    Log(f'executing {__file__}')
    dataFile = Build()
    dataFile.runbuild()
