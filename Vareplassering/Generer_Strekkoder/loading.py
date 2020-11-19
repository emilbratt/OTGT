import sys
from time import sleep

def loading_bar(count,total,barValue):
    sys.stdout.write("\033[F")
    print(f'\t{barValue}')
    # input()
    symbol = ''
    if total < 10:
        if count == total-1:
            print('Arbeider...')
            print(symbol.ljust(5, '|'))
            print('Ferdig')
            return count
        symbol = '|' * count
        print('Arbeider...')
        print(symbol.ljust(5, ' '))
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[F")
        return count
    elif total < 100:
        if count == 0:
            print('0%')
            print(symbol.ljust(50, '-'))
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")
            return count
        elif count == total-1:
            print('100%')
            print(symbol.ljust(50, '|'))
            print('Ferdig')
            return count
        else:
            progress = total/10
            add_bar = 0
            for i in range(1,11):
                if progress * i > count:
                    symbol = '|' * i*5
                    if i > 9:
                        i = 9
                    print(f'{i*10}%')
                    print(symbol.ljust(10, '-'))
                    sys.stdout.write("\033[F")
                    sys.stdout.write("\033[F")
                    return count
    else:
        if count == 0:
            print('0%')
            print(symbol.ljust(50, '-'))
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")
            return count
        elif count == total-1:
            print('100%')
            print(symbol.ljust(50, '|'))
            print('Ferdig')
            return count
        else:
            progress = total/100
            add_bar = 0
            for i in range(1,101):
                if i % 2 == 0:
                    add_bar += 1
                if progress * i > count:
                    symbol = '|' * add_bar
                    if i > 99:
                        i = 99
                    print(f'{i}%')
                    print(symbol.ljust(50, '-'))
                    sys.stdout.write("\033[F")
                    sys.stdout.write("\033[F")
                    return count
