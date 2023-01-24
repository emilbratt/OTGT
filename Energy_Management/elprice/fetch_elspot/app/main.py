from timehandle import sleep, timeofday, isodate
from envars     import envar_get

from httpdatastore   import httpdatastoreinit
from nordpooldayahead import nordpooldayaheadinit

class Application:

    STEP_DESC = {
        1: 'Sleeping until next clock hour',
        2: 'Fetching tomorrows prices from nordpool',
        3: 'Confirming correct date',
        4: 'Confirming correct currency',
        5: 'Confirming correct unit',
        6: 'Reshaping raw data to our format',
        7: 'Sending raw data',
        8: 'Sending reshaped data',
    }

    def __init__(self):
        print('Application starttime', isodate.today_minutes())
        self.nordpool = nordpooldayaheadinit(envar_get)
        self.http_transfer = httpdatastoreinit(envar_get)
        self.step = 1
        self.fresh_restarts = 0
        self.re_try = False
        self.re_try_counter = 0
        self.fetch_hour = int(envar_get('NORDPOOL_FETCH_HOUR'))
        # skip step 1 to include fetching first round if passed fetch_hour time
        if timeofday.hour() >= self.fetch_hour:
            self.step = 2

    def run(self):
        '''
            each step represents one task, the next task might depend on it

            if one task fails, we halt for a bit and depending on task,
            we keep re-trying a previous task or error out

        '''
        last_step = self.step
        print('---Step ' + str(self.step) + '---')
        print(self.STEP_DESC[self.step])
        match self.step:
            case 1:
                print('time now', timeofday.now())
                hour = sleep.until_next_hour()
                if hour >= self.fetch_hour:
                    self.step = 2
            case 2:
                if self.nordpool.fetch():
                    self.step = 3
                else:
                    self.re_try = True; self.step = 2
            case 3:
                if self.nordpool.confirm_date(isodate.today_plus_days(-1)):
                    self.step = 4
                else:
                    self.re_try = True; self.step = 2
            case 4:
                if self.nordpool.confirm_currency():
                    self.step = 5
                else:
                    self.re_try = True; self.step = 2
            case 5:
                if self.nordpool.confirm_unit():
                    self.step = 6
                else:
                    self.re_try = True; self.step = 2
            case 6:
                if self.nordpool.reshape_data():
                    self.step = 7
                else:
                    self.re_try = True; self.step = 2
            case 7:
                if self.http_transfer.send_raw(self.nordpool.data_raw):
                    self.step = 8
                else:
                    self.re_try = True; self.step = 7
            case 8:
                if self.http_transfer.send_reshaped(self.nordpool.data_reshaped):
                    self.step = 1
                else:
                    self.re_try = True; self.step = 8
            case _:
                print('some weird behavior occured, value for self.step =', self.step)
                exit(1)

        # after x fresh restarts, exit -> this service needs attention/update
        if self.fresh_restarts > 5:
            exit(last_step)

        # if a step has taken multiple re-tries, error out and start fresh
        if self.re_try_counter > 5:
            print('start fresh because error on step', last_step)
            self.step = 1
            self.re_try_counter = 0
            self.fresh_restarts += 1
            return False

        # if a step needs a re-try, halt until next 15 minute mark
        if self.re_try:
            print('re-run from step', self.step, 'because of failed step', last_step)
            self.re_try = False
            self.re_try_counter += 1
            sleep.until_next_quarter_hour()
            return False

        return True

def mainloop():
    app = Application()
    while 'I`m waiting for coffee':
        app.run()

mainloop()
