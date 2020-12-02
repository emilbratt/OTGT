#!/usr/bin/env python3
from time import sleep
from datetime import datetime
import os
import json
import calendar
from log import Log


# create clear screen function
clearScreen = lambda : os.system(
    'cls' if os.name == 'nt' else 'clear')

timeStampBegin = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")[:-4]
startDate = datetime.now().strftime("%Y-%m-%d")
mainPath = os.path.dirname(os.path.realpath(__file__))
dataPath = os.path.join(mainPath, "data")
dataJson = os.path.join(mainPath, "data", "db.json")

def getWeekDay(date):
    weekDays=["Mandag","Tirsdag","Onsdag","Torsdag",
        "Fredag","Lørdag","Søndag"]
    try:
        dayNumber = calendar.weekday(int(date[6:]), int(date[3:5]), int(date[:2]))
    except TypeError:
        dayNumber = date.weekday()
    return weekDays[dayNumber]




def workCalc(date,start,end):
    workedHours = int(end[:2]) - int(start[:2])
    workedMins = int(end[3:5]) - int(start[3:5])

    if workedHours < 0:
        return False

    if workedMins < 0:
        workedHours -= 1
        workedMins = (workedMins + 60)
    hours = str(workedHours)
    minutes = str(workedMins)
    print('\n\tRegistrert tid:\n\t' +
    getWeekDay(date) + ' '+ date + '\n\tfra ' +
    start + '\n\ttil ' + end + '\n\tJobbet ' +
    hours + ' timer og ' + minutes + ' minutter')

    isOK = input('\n\tStemmer dette?\n\t1. ja\n\t2. nei\n\tskriv: ')
    if isOK == '1':
        return True
    else:
        return False


def clockCalc():
    pass

def dateCalc():
    pass

def getDate():
    return int(datetime.now().strftime("%Y%m%d"))

def createDB():
    # create new db.json if none
    db = {}
    print('\tIngen brukere eksisterer')
    while True:
        username = input('\tSkriv inn brukernavn for å legge til\n\t')
        if username.isdecimal():
            username = input('\n\tBruke bokstaver')
        else:
            print(f'\t{username} blir lagt til, er dette OK?')
            isOK = input('\t1. ja\n\t2. nei\n\tskriv: ')
            if isOK == '1':
                break
    db['1'] = {'user':username, 'work':{}}
    if os.path.isfile(dataJson) == False:
        with open(dataJson, 'a') as loadFile:
            json.dump(db, loadFile, indent=2)
    return db

# write changes to database
def updateDB(db):
    with open(dataJson, 'w',encoding='utf-8') as loadFile:
        json.dump(db, loadFile, indent=2)

def loadDB(dataLog):
    try:
        loadFile = open(dataJson,encoding='utf-8')
        try:
            db = json.load(loadFile) # everything OK
        except json.decoder.JSONDecodeError:
            # force create new database and user
            dataLog.add('json.decoder.JSONDecodeError'+
                'on ./data/db.json, new file created')
            db = createDB()
            updateDB(db)
        loadFile.close()
    except FileNotFoundError:
        # force create new database and user
        dataLog.add('FileNotFoundError on ./data/db.json, '+
            'new file created')
        db = createDB()
        updateDB(db)
    # force create database and user
    if db == {}:
        db = createDB()
        updateDB(db)
    return db



class Database:
    def __init__(self,user='main'):
        self.currentUser = user
        self.dataLog = Log(user)

        # if no datadir, create new
        os.makedirs(dataPath, exist_ok=True)
        self.db = loadDB(self.dataLog)
        for id in self.db:
            if self.db[id]['user'] == user:
                self.id = id
    # init end


    def showUsers(self):
        print('\tid\tnavn')
        for id in self.db:
            print(f'\t{id}\t{self.db[id]["user"]}')


    def getUserName(self):
        return self.currentUser


    def choseUser(self, id):
        while True:
            try:
                self.dataLog = Log(self.db[id]["user"])
                return self.db[id]["user"]
            except KeyError:
                return None


    def addWork(self):
        print(f'\n\tRegistrere timer for {self.currentUser}')
        isOK = input(f'\n\t1. ja\n\t2. nei\n\tskriv:  ')
        if isOK != '1':
            return None
        while True:
            clearScreen()
            print(f'\n\tDato i dag:\t')
            print('\t' + getWeekDay(datetime.now())+ ' ' +
                datetime.now().strftime("%d.%m.%Y"))
            print('\n\tSkriv 1 for å bruke dagens dato'+
                '\n\teller tast inn egen dato'+
                '\n\tskriv 0 for å gå til hovedmeny')
            while True:
                date = input('\n\tFromatet må være slik: 01.01.2020'+
                    '\n\tskriv: ')
                if date == '1':
                    date = datetime.now().strftime("%d.%m.%Y")
                    break
                elif date == '0':
                    return None
                else:
                    try:
                        datetime.strptime(date, '%d.%m.%Y')
                        clearScreen()
                        print('\n\tDato som er registrert:')
                        print('\t' +getWeekDay(date)+ ' ' +date)
                        print('\ter dette OK?')
                        isOK = input('\t1. ja\n\t2. nei\n\tskriv: ')
                        if isOK == '1':
                            break
                    except ValueError:
                        input('\tUgyldig format'+
                            '\n\tTrykk Enter for å fortsette')
                        clearScreen()
            while True:
                clearScreen()
                print('\n\tSkriv start tid\n\tFormatet må være slik:')
                start = input('\t08:00\n\tskriv: ')
                if len(start) != 5:
                    input('\tUgyldig format'+
                        '\n\tTrykk Enter for å fortsette')
                    continue
                try:
                    datetime.strptime(start, '%H:%M')
                    break
                except ValueError:
                    input('\tUgyldig format'+
                        '\n\tTrykk Enter for å fortsette')
                    continue
            while True:
                clearScreen()
                print('\n\tSkriv slutt tid\n\tFormatet må være slik:')
                end = input('\t16:00\n\tskriv: ')
                if len(end) != 5:
                    input('\tUgyldig format'+
                        '\n\tTrykk Enter for å fortsette')
                    continue
                if end.replace(':','') <= start.replace(':',''):
                    print('\tslutt-tiden må være etter start-tiden')
                    input('\tTrykk Enter for å gå tilbake til hovedmeny')
                    return None
                try:
                    datetime.strptime(end, '%H:%M')
                    break
                except ValueError:
                    input('\tUgyldig format'+
                        '\n\tTrykk Enter for å fortsette')
                    continue

            clearScreen()

            # prompt user confirmation
            # check valid time
            if workCalc(date,start,end) == True:
                break
            else:
                continue

        clearScreen()

        y = date[6:]
        m = date[3:5]
        d = date[:2]
        if self.db[self.id]['work'] == {}:
            self.db[self.id]['work'][date[6:]] = {}
        if date[6:] not in self.db[self.id]['work']:
            self.db[self.id]['work'][date[6:]] = {}
        if date[3:5] not in self.db[self.id]['work'][date[6:]]:
            self.db[self.id]['work'][date[6:]][date[3:5]] = {}


        # if self.db[self.id]['work'] == {}:
        #     self.db[self.id]['work'][date[6:]] = {}
        # if date[6:] in self.db[self.id]['work']:
        #     pass
        # else:
        #     self.db[self.id]['work'][date[6:]] = {}
        #
        # if date[3:5] in self.db[self.id]['work'][date[6:]]:
        #     pass
        # else:
        #     self.db[self.id]['work'][date[6:]][date[3:5]] = {}

        if date[:2] in self.db[self.id]['work'][date[6:]][date[3:5]]:
            clearScreen()
            print('\n\tDu har allerede registrert arbeid for')
            print(f'\t{getWeekDay(date)} {date}\n')
            print('\tDitt gamle klokkeslett er:')
            print(f"\tFra {self.db[self.id]['work'][date[6:]][date[3:5]][date[:2]]['start']}")
            print(f"\tTil {self.db[self.id]['work'][date[6:]][date[3:5]][date[:2]]['end']}")
            print(f'\n\tDitt nye klokkeslett er:\n\tFra {start}\n\tTil {end}')
            choice = input('\n\tHvilket klokkeslett er riktig?'+
                '\n\t1. det gamle\n\t2. det nye\n\tskriv: ')
            if choice == '2':
                self.db[self.id]['work'][date[6:]][date[3:5]][date[:2]]['start'] = start
                self.db[self.id]['work'][date[6:]][date[3:5]][date[:2]]['end'] = end
            else:
                return None
        else:
            self.db[self.id]['work'][date[6:]][date[3:5]][date[:2]] = {'start':start,'end':end}

        self.dataLog.add(f'{self.currentUser}-{date}-{start}-{end}')
        updateDB(self.db)
        return None


    def addUser(self):
        while True:
            print('\n\tSkriv inn brukernavnet som du\n\t'+
                'ønsker å legge til\n\teller skriv 0 for å gå tilbake')
            name = input('\tskriv: ')
            if name == '0':
                return None

            for value in self.db.values():
                if name in value['user']:
                    print(f'\tBrukernavn {name} eksisterer allerede')
                    input('\tTrykk Enter for å gå videre')# exists = False
                    return None

            print(f'\n\t{name} blir lagt til, er dette OK?')
            choice = input('\t1. ja\n\t2. nei\n\tskriv: ')
            if choice == '1':
                self.dataLog.add(f'Added user {name}')
                if self.db == {}:
                    self.db['1'] = {'user':name, 'work':{}}
                    input('tom')
                else:
                    for i in range(1, int(max(self.db))+2):
                        if str(i) in self.db:
                            continue
                        else:
                            self.db[str(i)] = {'user':name, 'work':{}}
                            break
                    # self.db[str(int(max(self.db))+1)] = {'user':name}
                updateDB(self.db)
                return None
            else:
                return None


    def removeUser(self, userID):
        if userID in self.db:
            print('\tvil du virkelig fjerne')
            print(f'\t{self.db[userID]["user"]}')
            choice = input('\t1. ja\n\t2. nei\n\tskriv: ')
            if choice == '1':
                self.dataLog.add(f'Removed user {self.db[userID]["user"]}')
                del self.db[userID]
                updateDB(self.db)

        else:
            print(f'\tBruker med id {userID} eksisterer ikke')
            input('\tTrykk Enter for å gå videre')



# example usage
if __name__ == '__main__':
    Database().addWork()
    exit()
    def example():
        db = Database() # db object with no users chosen
        db.addUser('mike')
        db.showUsers()
        user_id = input('\tchose user: ')
        user_name = db.choseUser(user_id)
        if user_name == None:
            print(f'\tIngen bruker med id nr {user_id}')
        else:
            print(f'\tBruker {user_name} er valgt')
            db = Database(user_name) # db object with new user chosen

    example()
    exit()
