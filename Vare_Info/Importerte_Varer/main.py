#!/usr/bin/env python3
import os
import csv
from dbclient import *
from prettyquery import prettysql


if __name__ == '__main__':
    # set working directory
    appRootPath = os.path.dirname(os.path.realpath(__file__))

    os.makedirs('%s/importert' % appRootPath, exist_ok=True)
    c = connect()
    data = c.getToday()


    for row in prettysql(data):
        print(row)



    c.close()
