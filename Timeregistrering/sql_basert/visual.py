import os
import random
from time import sleep
# create clear screen function
clearScreen = lambda : os.system(
    'cls' if os.name == 'nt' else 'clear')


def enterContinue():
    input('\n\tTrykk Enter for å gå videre')

def emptyQuery(V,M):
    if V == []:
        message(M)
        enterContinue()
        return True


def messages(L):
    print('\n\t')
    for i in L:
        print('\t'+L[i])

def message(M):
    print('\n\t'+M)

def userConfirm(M,c=False):
    print()
    lines = ('\t+'+('-'*(len(M)+1))+'+')
    print(lines)
    print('\t| '+M+'|')
    print(lines)
    print('\t|'+'1. ja  2. nei'.center(len(M))+' |')
    print(lines)
    if input('\tskriv: ') == "1":
        if c == True:
            clearScreen()
        return True
    else:
        clearScreen()
        return False


def horisontalLine(n):
    print('+'+('-'*n)+'+')


def dictMatrix(D):
    w = 15 # column width
    for key in D:
        if len(D[key]) >= w:
            w = len(D[key])+2

        print(key)
    print(w)


def getUserValue(N,M=[],c=False):
 # N = numbers of columns to insert
 # M = Message
    LT = []
    while True:
        L = []
        for i in range(N):
            print('\n\t'+M[i])
            value = input('\n\tskriv: ')
            if value == '':
                message('Ingen verdier ble registrert\n\tAvslutter')
                enterContinue()
                return None
            L.append(value)
            if i == (N-1):
                L = tuple(L)
                LT.append(L)
                L = []
                return LT

def getUserValues(N,M=[],c=False):
 # N = numbers of columns to insert
 # M = Message
    LT = []
    while True:
        L = []
        for i in range(N):
            print('\n\t'+M[i])
            value = input('\n\tskriv: ')
            if value == '':
                message('Ingen verdier ble registrert\n\tAvslutter')
                enterContinue()
                return None
            L.append(value)
            if i == (N-1):
                L = tuple(L)
                LT.append(L)
                L = []
                if userConfirm('Vil du legge til flere verdier') == False:
                    return LT




# takes a list N (number of columns) 1 to 6
def listMatrix(H,inList,col,c=False):
    L = []
    if c == True:
        clearScreen()
    # append headers to first row
    for item in H:
        L.append(item)

    for items in inList:
        L.append(items)
    # print('\n\t'+H)
    w = 5 # column width
    for item in L:
        if len(str(item)) >= w:
            w = len(str(item))+2

    # add empty strings match grid
    while (len(L)%col) != 0 :
        L.append('')

    print() # force \n
    if col == 6:
        for i in range(0,len(L),col):
            print('\t+'+'-'*((w*6)+5)+'+')
            print(f'\t|{str(L[i]).center(w)}|{str(L[i+1]).center(w)}'
            + f'|{str(L[i+2]).center(w)}|{str(L[i+3]).center(w)}'
            +f'|{str(L[i+4]).center(w)}|{str(L[i+5]).center(w)}|')
        print('\t+'+'-'*((w*6)+5)+'+')
    elif col == 5:
        for i in range(0,len(L),col):
            print('\t+'+'-'*((w*5)+4)+'+')
            print(f'\t|{str(L[i]).center(w)}|{str(L[i+1]).center(w)}'
            + f'|{str(L[i+2]).center(w)}|{str(L[i+3]).center(w)}'
            +f'|{str(L[i+4]).center(w)}|')
        print('\t+'+'-'*((w*5)+4)+'+')
    elif col == 4:
        for i in range(0,len(L),col):
            print('\t+'+'-'*((w*4)+3)+'+')
            print(f'\t|{str(L[i]).center(w)}|{str(L[i+1]).center(w)}'
            + f'|{str(L[i+2]).center(w)}|{str(L[i+3]).center(w)}|')
        print('\t+'+'-'*((w*4)+3)+'+')
    elif col == 3:
        for i in range(0,len(L),col):
            print('\t+'+'-'*((w*3)+2)+'+')
            print(f'\t|{str(L[i]).center(w)}|{str(L[i+1]).center(w)}'
            + f'|{str(L[i+2]).center(w)}|')
        print('\t+'+'-'*((w*3)+2)+'+')
    elif col == 2:
        for i in range(0,len(L),col):
            print('\t+'+'-'*((w*2)+1)+'+')
            print(f'\t|{str(L[i]).center(w)}|{str(L[i+1]).center(w)}'
            + f'|')
        print('\t+'+'-'*((w*2)+1)+'+')
    elif col == 1:
        for i in range(0,len(L),col):
            print('\t+'+'-'*(w)+'+')
            print(f'\t|{str(L[i]).center(w)}|')
        print('\t+'+'-'*(w)+'+')

    # remove empty strings values
    while L[-1] == '':
        del L[-1]
    print() # force \n




# takes a list N (number of columns) 1 to 6
def tupleMatrix(H,T,col,c=False):
    if c == True:
        clearScreen()
    # print('\n\t'+M)
    w = 5 # column width
    L = [] # will be printed


    # append headers to first row
    for item in H:
        L.append(item)

    # extract individual values from tuple
    for item in T:
        for value in item:
            L.append(value)

    # get column width
    for item in L:
        if len(str(item)) >= w:
            w = len(str(item))+2

    # add empty strings match grid
    while (len(L)%col) != 0 :
        L.append('')

    print() # force \n
    if col == 6:
        for i in range(0,len(L),col):
            print('\t+'+'-'*((w*6)+5)+'+')
            print(f'\t|{str(L[i]).center(w)}|{str(L[i+1]).center(w)}'
            + f'|{str(L[i+2]).center(w)}|{str(L[i+3]).center(w)}'
            +f'|{str(L[i+4]).center(w)}|{str(L[i+5]).center(w)}|')
        print('\t+'+'-'*((w*6)+5)+'+')
    elif col == 5:
        for i in range(0,len(L),col):
            print('\t+'+'-'*((w*5)+4)+'+')
            print(f'\t|{str(L[i]).center(w)}|{str(L[i+1]).center(w)}'
            + f'|{str(L[i+2]).center(w)}|{str(L[i+3]).center(w)}'
            +f'|{str(L[i+4]).center(w)}|')
        print('\t+'+'-'*((w*5)+4)+'+')
    elif col == 4:
        for i in range(0,len(L),col):
            print('\t+'+'-'*((w*4)+3)+'+')
            print(f'\t|{str(L[i]).center(w)}|{str(L[i+1]).center(w)}'
            + f'|{str(L[i+2]).center(w)}|{str(L[i+3]).center(w)}|')
        print('\t+'+'-'*((w*4)+3)+'+')
    elif col == 3:
        for i in range(0,len(L),col):
            print('\t+'+'-'*((w*3)+2)+'+')
            print(f'\t|{str(L[i]).center(w)}|{str(L[i+1]).center(w)}'
            + f'|{str(L[i+2]).center(w)}|')
        print('\t+'+'-'*((w*3)+2)+'+')
    elif col == 2:
        for i in range(0,len(L),col):
            print('\t+'+'-'*((w*2)+1)+'+')
            print(f'\t|{str(L[i]).center(w)}|{str(L[i+1]).center(w)}'
            + f'|')
        print('\t+'+'-'*((w*2)+1)+'+')
    elif col == 1:
        for i in range(0,len(L),col):
            print('\t+'+'-'*(w)+'+')
            print(f'\t|{str(L[i]).center(w)}|')
        print('\t+'+'-'*(w)+'+')

    # remove empty strings values
    while L[-1] == '':
        del L[-1]
    print() # force \n


if __name__ == '__main__':

    list = []
    for i in range(random.randint(14,27)):
        list.append(random.randint(1000,50000))

    listMatrix('Liste over tall',list,random.randint(1,6))
