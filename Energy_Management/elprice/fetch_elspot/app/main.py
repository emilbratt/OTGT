from timehandle import sleep, timeofday, isodate
from envars     import envar_get

from httpdatastore   import httpdatastoreinit
from nordpooldayahead import nordpooldayaheadinit

class Application:

    def __init__(self):
        print('Application starttime', isodate.today_minutes())
        self.nordpool = nordpooldayaheadinit(envar_get)
        self.http_transfer = httpdatastoreinit(envar_get)
        self.step = 1
        self.fetch_hour = int(envar_get('NORDPOOL_FETCH_HOUR'))
        # make sure to include today on first round if passed fetch_hour time
        if timeofday.hour() >= self.fetch_hour:
            self.step = 2

    def run(self):
        print('currently on step', self.step)
        match self.step:
            case 1:
                print('time now', timeofday.now())
                print('sleeping until next hour')
                hour = sleep.until_next_hour()
                if hour >= self.fetch_hour:
                    self.step = 2
            case 2:
                if self.nordpool.fetch():
                    self.step = 3
                else:
                    print('fetching failed')
                    print('status code')
                    print(self.nordpool.status_code)
                    exit(1)
            case 3:
                if self.nordpool.confirm_date(isodate.today()):
                    self.step = 4
                else:
                    print('date confirm failed')
                    exit(1)
            case 4:
                if self.nordpool.confirm_currency():
                    self.step = 5
                else:
                    print('currency confirm failed')
                    exit(1)
            case 5:
                if self.nordpool.confirm_unit():
                    self.step = 6
                else:
                    print('unit confirm failed')
                    exit(1)
            case 6:
                if self.nordpool.reshape_data():
                    self.step = 7
                else:
                    print('reshape failed')
                    exit(1)
            case 7:
                if self.http_transfer.send_raw(self.nordpool.data_raw):
                    self.step = 8
                else:
                    print('sending data.raw failed')
                    exit(1)
            case 8:
                if self.http_transfer.send_reshaped(self.nordpool.data_reshaped):
                    print(self.nordpool.data_reshaped)
                    self.step = 1
                else:
                    print('sending data.reshaped failed')
                    exit(1)
            case _:
                print('resetting step from', self.step, 'to 1')
                self.step = 1

        return True

def mainloop():
    app = Application()
    while 'I`m waiting for coffee':
        app.run()

mainloop()
