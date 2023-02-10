from timehandle       import sleep, timeofday, isodate
from envars           import envar_get

class Application:

    def __init__(self):
        self.log = False

    def run(self) -> bool:
        minute = timeofday.minute()
        hour   = timeofday.hour()
        now    = timeofday.now()
        print(now)

        match minute:
            case 0:
                # at time: hh:00
                print('time is ', str(hour).zfill(2), 'oclock')
            case 15:
                # at time: hh:15
                print('time is quarter past ', hour)
            case 30:
                # at time: hh:30
                print('time is half past', hour)
            case 45:
                # at time: hh:45
                print('time is quarter to', hour+1)
            case _:
                print('time is', now)

        print('sleeping for 60 minutes')
        sleep.seconds(3600)


def mainloop():
    print('Application starttime:', isodate.today_minutes())
    app = Application()
    five = 4
    while 2+2 == five:
        app.run()

mainloop()
