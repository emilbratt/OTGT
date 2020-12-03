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



# load database object

def mainLoop():

    dataFile = Database()

    # main menu
    while True:

        clearScreen()
        print('''
              C.I.Pedersen
            Timeregistrering
        ''')
        if dataFile.getUserName() == 'main':
            print('\tIngen bruker valgt\n')
        else:
            print(f'\tValgt bruker: {dataFile.getUserName()}\n')
        print('\t1. Velg bruker\n\t2. Registrer Arbeid'+
            '\n\t3. Fjern Arbeid\n\t4. Legg til bruker'+
            '\n\t5. Fjern Bruker\n\t0. Avslutt')
        mainMenu = input('\tVelg: ')
        try:
            if mainMenu == '1':
                clearScreen()

                while True:
                    print('\n\tVelg bruker fra listen')
                    dataFile.showUsers()
                    print('\n\t0 Gå tilbake')
                    userID = input('\tSkriv inn id: ')
                    if userID == '0':
                        break

                    # returns None of no id was found
                    userName = dataFile.choseUser(userID)

                    if userName == None:
                        if userID == '':
                            clearScreen()
                            continue
                        else:
                            print(f'\n\tIngen bruker med id nr {userID}')
                            input('\tTrykk Enter for å gå videre')
                            clearScreen()
                    else:
                        dataFile = Database(userName)
                        break
            elif mainMenu == '2':
                clearScreen()
                if dataFile.getUserName() == 'main':
                    input('\n\tVelg en bruker først\n\tTrykk Enter for å gå tilbake')
                    continue
                dataFile.addWork()
            elif mainMenu == '4':
                clearScreen()
                if dataFile.getUserName() == 'main':
                    input('\n\tVelg en bruker først\n\tTrykk Enter for å gå tilbake')
                    continue
                print('\n\tEksisterende brukere\n')
                dataFile.showUsers()
                dataFile.addUser()

            elif mainMenu == '5':
                clearScreen()
                if dataFile.getUserName() == 'main':
                    input('\n\tVelg en bruker først\n\tTrykk Enter for å gå tilbake')
                    continue
                print('\n\tFjern bruker fra listen\n')
                while True:

                    dataFile.showUsers()
                    print('\n\t0 Gå tilbake')
                    choice = input('\tSkriv: ')
                    if choice == '0':
                        clearScreen()
                        break
                    else:
                        dataFile.removeUser(choice)
                    break
            elif mainMenu == '3':
                clearScreen()
                if dataFile.getUserName() == 'main':
                    input('\n\tVelg en bruker først\n\tTrykk Enter for å gå tilbake')
                    continue
                dataFile.removeWork()
            elif mainMenu == '0':
                clearScreen()
                exit()
        except ValueError: # ignore all invalid values
            pass



def extractHours():
    pass


if __name__ == '__main__':
    # run app
    mainLoop()
