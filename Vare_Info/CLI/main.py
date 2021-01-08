#!/usr/bin/env python3
import os
import sys
import csv
from dbclient import *
from prettyquery import prettysql
from datetime import datetime
from spreadsheet import exportXLSX
# create a clear screen function
clearScreen = lambda : os.system(
    'cls' if os.name == 'nt' else 'clear')

# get timestamp and date
timestamp = datetime.now()
ymd = timestamp.strftime("%Y-%m-%d")


# set working directory
filePath = os.path.dirname(os.path.realpath(__file__))
outPath = os.path.join(filePath, 'Utskrift')
currentFile = os.path.join(outPath, (ymd+'.xlsx'))

# if no dir, create new
os.makedirs(outPath, exist_ok=True)

    # colours: # green     # red    # yellow   #turquoise  # purple   # blue
colourPrint = ["\033[92m","\033[91m","\033[93m","\033[96m","\033[95m","\033[94m"]



def openFile(path):
    if sys.platform.startswith('linux'):
        os.system('xdg-open "%s"' % path)
    elif sys.platform.startswith('win32'):
        import subprocess
        subprocess.Popen('explorer "%s"' % path)
    elif sys.platform.startswith('darwin'):
        os.system('xdg-open "%s"' % path)



def printAllTerminal():
    c = connect()
    clearScreen()
    data = c.getImportToday()
    c.close()
    prettysql(data)


def getImport():
    message = (f'{colourPrint[3]}\n\tFor hvilken dag?\n\t0 = idag\n\t1 = igår'+
        f'\n\t2 = forigårs osv..\n\t{colourPrint[2]}skriv: \033[0m')
    while True:
        days = input(message)
        if days.isnumeric():
            days = int(days)
            break
        else:
            print(f'{colourPrint[3]}\n\tSkriv inn et tall')



    c = connect()
    data = c.getImport(days)
    currentFile = os.path.join(outPath, (str(c.getYYYYMMDD(days))+'.xlsx'))
    c.close()


    spreadsheet = exportXLSX(currentFile, data)
    openFile(spreadsheet)


def printInfoTerminal(choice):
    clearScreen()
    c = connect()
    while True:
        # c = connect()

        while True:
            message = (f'{colourPrint[0]}'+
                f'Skan strekkode eller trykk Enter for å gå tilbake')
            barcode = input(message)
            sys.stdout.write("\033[F")
            if barcode.isnumeric():
                break
            elif barcode == 'exit':
                c.close()
                exit()
            elif barcode == '':
                c.close()
                return None

        if choice == '1':
            data = c.showSingleItemInfo(barcode)
        elif choice == '2':
            data = c.showSingleItemExtendedInfo(barcode)
        prettysql(data)


if __name__ == '__main__':
    while True:
        clearScreen()
        print(f'\n\t{colourPrint[0]}Vareoversikt\n\tVelg:\n\033[0m')
        print(f'\t{colourPrint[3]}'+
        f'1. Skann en og en vare og vis generell info på skjerm\033[0m')
        print(f'\t{colourPrint[3]}'+
        f'2. Skann en og en vare og vis utvidet info på skjerm\033[0m')
        print(f'\t{colourPrint[3]}'+
        f'3. Åpne oversikt over alle importerte varer i dag (regneark)\033[0m')
        print(f'\n\t{colourPrint[4]}'+
        f'0. Avslutt\033[0m')
        choice = input(f'\n\t{colourPrint[2]}skriv: \033[0m')


        if choice == '1':
            printInfoTerminal('1')
        elif choice == '2':
            printInfoTerminal('2')
        elif choice == '3':
            getImport()
        elif choice == '0':
            exit()
