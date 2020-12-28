#!/usr/bin/env python3
import os
import sys
import csv
from dbclient import *
from prettyquery import prettysql
from datetime import datetime

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


def exportXLSX():
    import openpyxl
    from openpyxl import Workbook
    from openpyxl.utils import get_column_letter
    from openpyxl.styles import Alignment

    # set working directory
    appRootPath = os.path.dirname(os.path.realpath(__file__))
    # os.makedirs('%s/utskrift' % appRootPath, exist_ok=True)
    c = connect()
    data = c.getImportToday()
    c.close()

    wb = Workbook()
    ws = wb.active

    for row in data:
        ws.append(list(row))

    for col in ws.columns:
        for cell in col:
            cell.alignment = Alignment(horizontal='center', vertical='center')

    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 25
    ws.column_dimensions['C'].width = 70
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 8
    ws.column_dimensions['F'].width = 8

    wb.save(currentFile)
    return currentFile



def printInfoTerminal(choice):
    clearScreen()
    c = connect()
    while True:
        # c = connect()

        while True:
            barcode = input('Skan strekkode eller trykk Enter for å gå tilbake')
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
        print(f'\t{colourPrint[3]}1. Skann en og en vare og vis generell info på skjerm\033[0m')
        print(f'\t{colourPrint[3]}2. Skann en og en vare og vis utvidet info på skjerm\033[0m')
        print(f'\t{colourPrint[3]}3. Åpne oversikt over alle importerte varer i dag (regneark)\033[0m')
        print(f'\n\t{colourPrint[4]}0. Avslutt\033[0m')
        choice = input(f'\n\t{colourPrint[2]}skriv: \033[0m')


        if choice == '1':
            printInfoTerminal('1')
        elif choice == '2':
            printInfoTerminal('2')
        elif choice == '3':
            currentFile = exportXLSX()
            openFile(currentFile)
        elif choice == '0':
            exit()
