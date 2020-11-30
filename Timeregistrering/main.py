#!/usr/bin/env python3
# Emil Bratt -> emilbratt@gmail.com
import os
import json

'''
    kalkulerer utbetaling basert på tidspunkt når ansatt jobbet
    den ansatte fyller inn start og slutt tid og eventuelt dato
'''


def leggTil():
    print('\n\tSkriv inn brukernavn (helst kun fornavn)\n\t'+
        'som du ønsker å legge til å trykk Enter')
    nameInput = input('\tskriv: ')
    print(nameInput)
    exit()






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

    # main menu
    while True:
        clearScreen()
        print('''
            C.I.Pedersen
            Timeregistrering
        ''')
        print('\t1. Legg til bruker\n\t2. Registrer timer\n\t3. Vis alle brukere\n\t4. Avslutt')
        V = input('\tVelg: ')
        try:
            if int(V) == 1:
                leggTil()
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
