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
        if dataFile.getCurrentUser() == 'main':
            print('\tIngen bruker valgt\n')
        else:
            print(f'\tValgt bruker: {dataFile.getCurrentUser()}\n')
        print('\t1. Velg bruker\n\t2. Registrer timer\n\t3. Se oversikt'+
            '\n\t4. Legg til bruker\n\t5. Fjern bruker\n\t0. Avslutt')
        choice = input('\tVelg: ')
        try:
            if int(choice) == 1:
                clearScreen()

                while True:
                    print('\n\tVelg bruker fra listen')
                    dataFile.showUsers()
                    print('\n\t\t0 Gå tilbake')
                    choice = input('\tSkriv inn id: ')
                    if choice == '0':
                        break
                    userName = dataFile.choseUser(choice)
                    if userName == None:
                        print(f'\tIngen bruker med id nr {choice}')
                        input('\tTrykk Enter for å gå videre')
                        clearScreen()
                    else:
                        dataFile = Database(userName)
                        break
            elif int(choice) == 2:
                clearScreen()
                if dataFile.getCurrentUser() == 'main':
                    input('\n\tVelg en bruker først\n\tTrykk Enter for å gå tilbake')
                    continue
                dataFile.addWork()
            elif int(choice) == 4:
                clearScreen()
                if dataFile.getCurrentUser() == 'main':
                    input('\n\tVelg en bruker først\n\tTrykk Enter for å gå tilbake')
                    continue
                print('\n\tEksisterende brukere')
                dataFile.showUsers()
                dataFile.addUser()

            elif int(choice) == 5:
                clearScreen()
                if dataFile.getCurrentUser() == 'main':
                    input('\n\tVelg en bruker først\n\tTrykk Enter for å gå tilbake')
                    continue
                print('\n\tFjern bruker fra listen')
                while True:

                    dataFile.showUsers()
                    print('\t0 Gå tilbake')
                    choice = input('\tSkriv: ')
                    if choice == '0':
                        break
                    else:
                        dataFile.removeUser(choice)
                    break

            # elif int(choice) == 4:
            #     pass
            #     # showUsers()
            elif int(choice) == 0:
                clearScreen()
                exit()
        except ValueError: # ignore all invalid values
            pass




def extractHours():
    pass


if __name__ == '__main__':
    # run app
    mainLoop()
