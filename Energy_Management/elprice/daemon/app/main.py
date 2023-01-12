from timehandle import sleep

def run_every_hour(hour: int) -> bool:
    print(hour)

    print('running function for every hour')

    if hour == 14:
        print('running function for 14:00')

    if hour == 0:
        print('running function for midnight (00:00)')

    return True


def main():
    print('running main')
    hour = sleep.until_next_hour()
    run_every_hour(hour)


while True:
    main()
