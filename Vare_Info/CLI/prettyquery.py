

def prettysql(records, colnames=''):
    '''
        this function takes a sqlite object or a list with tuples as first parameter
        and optionally a colname tuple with columnheaders that is specifically added

        the format should be like this:
        [('val','val','val'),('val','val','val'),]

        if the last values in a row is not present, the function
        will generate whitespace values so that the integrity of
        the matrix remains untouched

        this can be used as a pretty print of pythons sqlite3 queries

        feed the query-result of sqlite into this function
        and loop through the returned list

        each list-object holds one row making it easy
        to iterate through the results in a for loop

        an example usage:
        for row in prettysql(sqlResult):
            print(row)

    '''

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

    for row in printFormat:
        print(row)
    # return printFormat
    return None


# example usage
if __name__ == '__main__':

##################################################################

    # example with a sqlite3 instance

    import sqlite3

    # create som queries to build, insert and select from database
    createDummyTable = '''
    CREATE TABLE IF NOT EXISTS users(
        id     INTEGER PRIMARY KEY AUTOINCREMENT,
        user   TEXT NOT NULL,
        age   INTEGER DEFAULT 0,
        description    TEXT NOT NULL
        );
    '''

    insertDummyValues = '''
    INSERT INTO users (
        user,
        age,
        description
    )
    VALUES (
        ?,?,?
    );
    '''

    dummyValues = [
    ('bob', 30,'retail'),
    ('alice', 40,'accounting'),
    ('jack', 35,'inventory'),
    ]

    selectFromTable = '''
    SELECT * FROM users;
    '''

    colnames = (
    'user id','user name','age','description',
    )


    # execute queries
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute(createDummyTable)
    cursor.executemany(insertDummyValues,dummyValues)
    conn.commit()


    # this is how we use the prettysql statement
    # save result from select query into variable
    rows = cursor.execute(selectFromTable)

    # pass variable into function and iterate over result
    for row in prettysql(rows,colnames): # optional: pass the column names (tuple)
        print(row)

    # then we can close the connection
    conn.close()

##################################################################

    # example with a list with a missing value

    myRecords = [
    ('name','age','city'),
    ('bob','30','new york'),
    ('bob','30','new york'),
    ('ross','30','london'),
    ('alice','40','rome'),
    ('jon','26','berlin'),
    ('jane','20'),
    ]

    for row in prettysql(myRecords):
        print(row)

##################################################################

    # example with a list wih a random amount of rows and values

    import random

    genTuple = []
    genList = []
    rangeNum = random.randint(16,28)
    for i in range(rangeNum):

        if i % 5 == 0:
            if genList == []:
                continue
            else:
                genTuple.append(tuple(genList))
                genList = []
        num = str(random.randint(1000,50000))
        genList.append(num)
    if i == rangeNum-1:
        genTuple.append(tuple(genList))

    for row in prettysql(genTuple):
        print(row)

##################################################################
