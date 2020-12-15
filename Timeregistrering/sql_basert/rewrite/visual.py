

def prettysql(records, colnames=''):

    # extract tuples from parameters
    buildRows = []
    if colnames != '':
        buildRows.append(colnames) # if colames where passed, append row
    for row in records:
        buildRows.append(tuple(row))
    records = buildRows

    # get number of columns
    numColumns = len(records[0]) # get number of columns

    # loop through each value and set a column width based
    # on the length of the longest string in that column
    colWith = [] # column widths
    for col in records:
        for i,val in enumerate(col):
            try:
                if len(str(val)) >= colWith[i]-1:
                    colWith[i] = len(str(val))+2
            except IndexError:
                    colWith.insert(i, len(str(val))+2)

    breakLine = '+'

    # create the line that is between each printed record
    for i in range(numColumns):
        breakLine += '-'*(colWith[i])+'+'

    # append the formated strings to the print list
    printFormat = []
    for line,row in enumerate(records):
        addDummy = 0
        string = '|'

        for i in range(numColumns):
            try:
                string += str(row[i]).center(colWith[i])+'|'
            except IndexError:
                # add dummy values if the row has less
                # than values than columns
                string += ''.center(colWith[i])+'|'

        printFormat.append(breakLine)
        printFormat.append(string)

    printFormat.append(breakLine)

    return printFormat

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
