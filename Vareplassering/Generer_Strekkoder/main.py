#!/usr/bin/env python3
import csv
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
import os

# set working directory in a variable
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
        print('''\t1. Generer strekkoder interaktivt
\t2. Avslutte''')
        choice = input('\t\t' + 'Skriv: ')
        if choice.isdecimal() and int(choice) >= 1 and int(choice) <= 3:
            return int(choice)



def generateBarcodeValues(choice):

    print('\n\tNå skal vi laste inn alle verdiene vi ønsker å ha med')
    print('\tAlle bokstaver blir gjort om til store bokstaver')
    print('\tSkriv inn verdien du ønsker og trykk Enter (Maks 8 tegn)\n\t\
Når du er ferdig så lar du feltet stå tomt og trykker Enter')
    while True:
        values = []
        while True:
            value = input('\t\t' + 'Strekkode: ').upper()
            value = value
            values.append(value)
            if values[-1] == '':
                values.remove('')
                break

        while True:
            print(f'\n\tVerdiene du har skrevet inn er:\n')
            dummy = len(values)%6
            for i in range(6-dummy):
                values.append(' ')
            for i in range(len(values)-1):
                if i%6 == 0:
                    print(f'\t{values[i].ljust(8)}{values[i+1].ljust(8)}{values[i+2].ljust(8)}\
{values[i+3].ljust(8)}{values[i+4].ljust(8)}{values[i+5].ljust(8)}')
            for i in range(6-dummy):
                values.remove(' ')
            print('\n\tEr disse riktige?\n')
            choice = input('\t0. Start på nytt\n\t1. Fortsett\n\t3. Avslutt\n\t\tSkriv: ')
            if choice == '3':
                exit()
            if choice == '1' or choice == '0':
                break

        if choice == '1':
            break

    generateBarcodes(values)


def generateBarcodes(values):


    print('\tGenererer strekkoder...\n')
    try:
        fontUsed = ImageFont.truetype('arial.ttf', 72)
    except OSError:
        fontUsed = ImageFont.truetype(os.path.join(path, 'FreeSans.ttf'), 72)

    for iterate,barValue in enumerate(values):
        print(f'\t{barValue}')

        fileName = os.path.join(path, 'Strekkoder', barValue)

        # convert value to barValue
        Code128(barValue, writer=ImageWriter()).save(fileName)

        # open the barValue as image and start
        openBarcode = Image.open('%s.png' % fileName).convert('LA')


        if iterate%19 == 0:
            if iterate%38 == 0:
                # open a A4 size to pasted cropped versions
                A4sheet = Image.new('RGB', (1240,1754), (255, 255, 255))
                saveA4sheet = str(int(iterate/38)).zfill(len(str(int(len(values)/38))))
                pasteLeft = 50
            else:
                pasteLeft = 680

        pasteTop = (10 + (iterate%19) * 92)

        # open new blank where cropped version of original will be pasted
        cropped = Image.new('RGB', (560,80), (255, 255, 255))

        # Horizontal = openBarcode.size[0]
        # Vertical = openBarcode.size[1]
        cropValue = (0, 80, openBarcode.size[0], 160)
        # cropValue params: start pixel left, start pixel top, end pixel right, end pixel bottom

        croppedRegion = openBarcode.crop(cropValue)
        cropped.paste(croppedRegion, (250,0))
        # paste values represents: (pxiels from left, pixels from top)

        # add text next to barcode (left side)
        textInput = ImageDraw.Draw(cropped)
        textInput.text((0,0), barValue, font=fontUsed, fill=(0, 0, 0))

        A4sheet.paste(cropped, (pasteLeft,pasteTop))

        openBarcode.close()
        cropped.close()

        os.remove('%s.png' % fileName)

        if iterate%38 == 37 or iterate == len(values)-1:
            A4sheet.save('%s.png' % os.path.join(path, 'Strekkoder', saveA4sheet))
            A4sheet.close()

    print('Ferdig')



if __name__ == '__main__':
    choice = mainMenu()
    if choice == 2:
        exit()
    generateBarcodeValues(choice)
