#!/usr/bin/env python3
import subprocess
import sys

import requests
import configparser
import os
import json

import Database

def mainloop():
    while True:
        jobs = Database.SelectJobsToday()
        print(jobs.res)
        exit()

if __name__ == '__main__':
    mainloop()
