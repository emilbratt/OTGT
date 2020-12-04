import os
import random
# create clear screen function
clearScreen = lambda : os.system(
    'cls' if os.name == 'nt' else 'clear')



def continueAsk():
    print('\n\tVil du fortsette?\n\t1. ja\n\t2. nei')
    if input() == "1":
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



# takes a list N (number of columns) 1 to 6
def listMatrix(L,col):
    clearScreen()
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
def tupleMatrix(T,col):
    clearScreen()
    w = 5 # column width
    L = []

    # extract individual values from tuple
    for item in T:
        for value in item:
            L.append(value)
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

    listMatrix(list,random.randint(1,6))
