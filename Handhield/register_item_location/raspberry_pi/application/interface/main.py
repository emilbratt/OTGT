#!/usr/bin/env python3


from LEDReporter.LEDR import LEDR
from Database.Jobs import Jobs

def main():
    ledr = LEDR()
    jobs = Jobs()
    print(ledr.led)

if __name__ == '__main__':
    main()
