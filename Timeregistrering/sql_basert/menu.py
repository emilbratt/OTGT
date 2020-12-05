from visual import dictMatrix
        #     print(f'\tValgt bruker: {dataFile.getUserName()}\n')
        # print('\t1. Velg bruker\n\t2. Registrer Arbeid'+
        #     '\n\t3. Fjern Arbeid\n\t4. Legg til bruker'+
        #     '\n\t5. Fjern Bruker\n\t0. Avslutt')


mainMenu = {
'1':'Velg Bruker',
'2':'Registrer timer',
'3':'Fjern registrerte timer',
'4':'Legg til bruker',
'5':'Fjern bruker',
'6':'Avslutt'
}


if __name__ == '__main__':
    dictMatrix(mainMenu)
    # list = ['hei','hade','morn','emil','john','kåre','jan']
