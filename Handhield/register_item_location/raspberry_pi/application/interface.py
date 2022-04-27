#!/usr/bin/env python3
import subprocess
import sys
# import requests
import configparser
import os
import json

from LEDReporter.LEDR import LEDR
import Database


def mainloop():
    while True:
        ledr = LEDR()
        # print(dir(Database))
        print(ledr.led)
        exit()

def main():
    Database.CreateTables()
    mainloop()

if __name__ == '__main__':
    main()
