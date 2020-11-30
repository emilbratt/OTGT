#!/usr/bin/env python3
# Emil Bratt -> emilbratt@gmail.com
import os
import json

'''
    kalkulerer utbetaling basert på tidspunkt når ansatt jobbet
    den ansatte fyller inn start og slutt tid og eventuelt dato
'''


def addUser():
    # try:
    pass
        # mode = open('%s/data/users.json'%path,encoding='utf-8')
        # debug = json.load(mode)
        # mode.close()


def mainLoop():
    '''initialize start'''
    # fetch full path for __file__, data and log
    mainPath = os.path.dirname(os.path.realpath(__file__))
    dataPath = os.path.join(mainPath, "data")
    logPath = os.path.join(mainPath, "log")

    # force create data and log directory if none
    os.makedirs(dataPath, exist_ok=True)
    os.makedirs(logPath, exist_ok=True)

    # fetch path for users.json
    usersJson = os.path.join(
        mainPath, "data", "users.json"
        )

    # create new users.json if none
    if os.path.isfile(usersJson) == False:
        with open(usersJson, 'a') as newJsonFile:
            newJsonFile.write("{}")

    # load users
    with open(usersJson,encoding='UTF-8') as jsonFile:
        users = json.load(jsonFile)

    # create a function that clears the terminal output
    clearScreen = lambda : os.system(
        'cls' if os.name == 'nt' else 'clear')

    clearScreen()
    '''initialize finish'''
    # main options
    print('''
        C.I.Pedersen
        Timeregistrering
    ''')
    print('\t1. Legg til bruker\n\t2. Registrer timer\n\t3. Vis alle brukere\n\t4. Avslutt')
    V = input('\tVelg: ')
    while True:
        try:
            if int(V) == 1:
                addUser()
                break
            elif int(V) == 2:
                break
                # regHour()
            elif int(V) == 3:
                break
                # showUsers()
            elif int(V) == 4:
                clearScreen()
                exit()

        except ValueError: # handle int error if input = str
            pass
        V = input('\tVelg et alternativ')



def extractHours():
    pass


if __name__ == '__main__':
    # run app
    mainLoop()
