#!/usr/bin/env python3
# Emil Bratt -> emilbratt@gmail.com
import webbrowser
import csv
import os
from loading import loading_bar
import subprocess
import sys
from barcode.writer import ImageWriter
from barcode import Code128
from PIL import Image, ImageDraw, ImageFont

# set working directory
path = os.path.dirname(os.path.realpath(__file__))


def mainMenu():
    os.makedirs('%s/Strekkoder' % path, exist_ok=True)
    os.makedirs('%s/CSV' % path, exist_ok=True)
    while True:
        print('\n' * 10)
        print('''
                  ------------------
                  ----Strekkoder---
                  --------av--------
                  ----Emil-Bratt----
                  ------------------
        ''')
        print('\t\tHva ønsker du å gjøre?\n')
        print('\t1. Generer strekkoder interaktivt'
        + '\n\t2. Generer strekkoder fra csv-fil'
        + '\n\t3. Avslutte')
        choice = input('\t\t' + 'Skriv: ')
        if choice.isdecimal() and int(choice) >= 1 and int(choice) <= 3:
            return int(choice)




def generateBarcodeValues(choice):

    if choice == 1:

        print('\tSkriv inn verdien du ønsker og trykk Enter (Maks 7 tegn)'
        +'\n\tNår du er ferdig så lar du feltet stå tomt og trykker Enter')
        print('\tAlle bokstaver blir gjort om til store bokstaver')
        while True:
            values = []
            while True:
                value = input('\t\t' + 'Strekkode: ').upper()
                if len(value) > 7:
                    print('\t\tKan ikke ha mere enn 7 tegn')
                    continue
                if values == [] and value == '':
                    continue
                values.append(value)

                if values[-1] == '':
                    values.remove('')
                    break

            while True:
                print(f'\n\tVerdiene du har skrevet inn er:\n')
                fitLength = len(values)%6

                # add dummy values so that the matrix will display correctly
                while len(values)%6 != 0:
                    values.append('')

                # show matrix (grid) and iterate 6 items for each row
                for i in range(len(values)-1):
                    if i%6 == 0:
                        print('\t'+'-'*61)
                        print(f'\t|{values[i].center(9)}|{values[i+1].center(9)}'
                        + f'|{values[i+2].center(9)}|{values[i+3].center(9)}'
                        +f'|{values[i+4].center(9)}|{values[i+5].center(9)}|')
                print('\t'+'-'*61)

                # remove dummy values
                while values[-1] == '':
                    del values[-1]
                print('\n\tEr disse riktige?\n')
                choice = input('\t0. Start på nytt\n\t1. Fortsett\n\t2. Avslutt\n\t\tSkriv: ')
                if choice == '2':
                    exit()
                if choice == '1' or choice == '0':
                    break

            if choice == '1':
                break

    elif choice == 2:
        print(f'\n\tLegg csv filen i mappen:\n\t{os.path.join(path, "CSV")}')
        input('\n\tFor å åpne mappen trykk Enter: ')
        if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            os.system('xdg-open "%s"' % os.path.join(path, "CSV"))
        elif sys.platform.startswith('win32'):
            subprocess.Popen('explorer "%s"' % os.path.join(path, "CSV"))

        input('\n\tNår du har lagt csv-filen i mappen så trykker du Enter: ')

        while True:
            listCSV = [f for f in os.listdir(os.path.join(path, 'CSV'))
            if os.path.splitext(f)[-1] == '.csv']

            if len(listCSV) == 0:
                input('\n\tFant ingen filer\n\t0. Søke på nytt\n\t1.Avslutte\n\tSkriv: ')
                if choice == '0':
                    continue
                elif choice == '1':
                    exit()
            elif len(listCSV) != 0:
                print(f'\n\t{len(listCSV)} filer ble funnet:')
                for iterate,file in enumerate(listCSV):
                    print(f'\t\t{iterate+1} -> {file}')
                choice = input('\n\tVelg fil\n\t0. Avslutt\n\t\tSkriv: ')
                if int(choice) > len(listCSV) or int(choice) < 0:
                    input('\n\tNummeret finnes ikke\n\t\tTrykk Enter: ')
                elif choice == '0':
                    exit()
                elif int(choice) <= len(listCSV) or int(choice) > 0:
                    break
                    # continues if valid file was selected

        readCSV = open(os.path.join(path,
        'CSV', str(listCSV[(int(choice)-1)])),
        encoding='utf-8')

        if ';' in readCSV.readline():
            separation = ';'
        else:
            separation = ','
        readCSV.close()
        with open(os.path.join(path, 'CSV', str(listCSV[(int(choice)-1)])),
        encoding='utf-8') as readCSV:
            readerobject = csv.reader(readCSV,delimiter=separation)
            values = []
            for row in readerobject:
                if len(''.join(row)) > 7:
                    print('\tcsv-filen har strekkoder som er lengre enn 7 tegn'
                    +'\n\trett opp csv-filen før du prøver igjen'
                    +'\n\tavslutter..')
                    exit()
                values.append(''.join(row))

    generateBarcodes(values)


def generateBarcodes(values):


    print('\n\tGenererer strekkoder...\n')
    try:
        fontUsed = ImageFont.truetype('arial.ttf', 72)
    except OSError:
        fontUsed = ImageFont.truetype(os.path.join(path, 'FreeSans.ttf'), 72)

    for iterate,barValue in enumerate(values):

        fileName = os.path.join(path, 'Strekkoder', barValue)

        # convert value to barcode value
        Code128(barValue, writer=ImageWriter()).save(fileName)

        # open the barcode value as image and start
        openBarcode = Image.open('%s.png' % fileName).convert('L')


        if iterate%19 == 0:
            if iterate%38 == 0:
                # open an A4 size to pasted cropped versions
                A4sheet = Image.new('RGB',(1240,1754),
                (255, 255, 255)
                ).convert('L')
                saveA4sheet = str(
                int(iterate/38)
                ).zfill(len(str(int(
                len(values)/38
                ))))
                pasteLeft = 50
            else:
                pasteLeft = 680

        pasteTop = (10 + (iterate%19) * 92)

        # open new blank where cropped version of original will be pasted
        cropped = Image.new('RGB', (560,80), (255, 255, 255))

        # Horizontal = openBarcode.size[0]
        # Vertical = openBarcode.size[1]
        cropValue = (0, 80, openBarcode.size[0], 160)
            # params:
                # start pixel left, start pixel top
                # end pixel right, end pixel bottom

        croppedRegion = openBarcode.crop(cropValue)
        cropped.paste(croppedRegion, (250,0))
        # paste values represents: (pxiels from left, pixels from top)

        textInput = ImageDraw.Draw(cropped)
        textInput.text((0,0), barValue.rjust(7), font=fontUsed, fill=(0, 0, 0))

        A4sheet.paste(cropped, (pasteLeft,pasteTop))

        openBarcode.close()
        cropped.close()

        os.remove('%s.png' % fileName)

        if iterate%38 == 37 or iterate == len(values)-1:
            A4sheet.save('%s.png' % os.path.join(
            path, 'Strekkoder', saveA4sheet))
            A4sheet.close()

        if sys.platform.startswith(
        'linux'
        ) or sys.platform.startswith(
        'darwin'
        ):
            loading_bar(iterate, len(values),barValue)
        elif sys.platform.startswith(
        'win32'
        ):
            print(fileName)

    openFolder(os.path.join(path, 'Strekkoder'))

def openFolder(path):
    if sys.platform.startswith('linux'):
        os.system('xdg-open "%s"' % path)
    elif sys.platform.startswith('win32'):
        subprocess.Popen('explorer "%s"' % path)
    elif sys.platform.startswith('darwin'):
        os.system('xdg-open "%s"' % path)



if __name__ == '__main__':
    choice = mainMenu()
    if choice == 3:
        exit()
    generateBarcodeValues(choice)
