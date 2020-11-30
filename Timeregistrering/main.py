#!/usr/bin/env python3
# Emil Bratt -> emilbratt@gmail.com
import os
# import json
from data import Database
'''
    kalkulerer utbetaling basert på tidspunkt når ansatt jobbet
    den ansatte fyller inn start og slutt tid og eventuelt dato
'''

# create clear screen function
clearScreen = lambda : os.system(
    'cls' if os.name == 'nt' else 'clear')

def velgBruker(dataFile):
    clearScreen()
    print('\n\tVelg bruker fra listen')
    while True:


        print('\t    0 Avslutt')
        dataFile.showUsers()
        choice = input('\tSkriv: ')
        userName = dataFile.choseUser(choice)
        if userName == None:
            print(f'\tIngen bruker med id nr {choice}')
        else:
            print(f'\tBruker {userName} er valgt')
            return userName

def leggTilBruker():
    print('\n\tSkriv inn brukernavn (helst kun fornavn)\n\t'+
        'som du ønsker å legge til å trykk Enter')
    nameInput = input('\tskriv: ')
    dataFile.addUser(nameInput)




# load database object
dataFile = Database()
def mainLoop():
    '''initialize start'''
    # # fetch full path for __file__, data and log
    # mainPath = os.path.dirname(os.path.realpath(__file__))
    # dataPath = os.path.join(mainPath, "data")
    # logPath = os.path.join(mainPath, "log")

    # # force create data and log directory if none
    # os.makedirs(dataPath, exist_ok=True)
    # os.makedirs(logPath, exist_ok=True)



    '''initialize finish'''


        # '\n\t3. Registrer timer\n\t4. Vis alle brukere\n\t5. Avslutt')
    # main menu
    while True:
        clearScreen()
        print('''
              C.I.Pedersen
            Timeregistrering
        ''')
        print('\t1. Velg bruker \n\t2. Legg til bruker')
        choice = input('\tVelg: ')
        try:
            if int(choice) == 1:
                currentUser = velgBruker(dataFile)
                # currentUser = Database(choice)
            elif int(choice) == 2:
                leggTilBruker()
                # break
            elif int(choice) == 3:
                break
                # regHour()
            elif int(choice) == 4:
                break
                # showUsers()
            elif int(choice) == 5:
                clearScreen()
                exit()
            input('\tTrykk Enter for å gå videre')
        except ValueError: # handle int error if input = str
            pass
        # choice = input('\tVelg et alternativ')



def extractHours():
    pass


if __name__ == '__main__':
    # run app
    mainLoop()
