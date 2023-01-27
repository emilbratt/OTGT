from timehandle       import sleep, timeofday, isodate
from envars           import envar_get
from httpdatastore    import httpdatastoreinit
from nordpooldayahead import nordpooldayaheadinit

class Application:

    STEP_DESC = {
        1: 'Sleeping until fetch time',
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

        self.re_try = False
        self.re_try_counter = 0
        self.fresh_restarts = 0

        self.fetch_hour = int(envar_get('NORDPOOL_FETCH_HOUR'))
        self.fetch_minute = int(envar_get('NORDPOOL_FETCH_MINUTE'))

        if timeofday.is_passed_time(hour=self.fetch_hour, minute=self.fetch_minute):
            self.step = 2
        else:
            self.step = 1

    def run(self) -> bool:
        '''
            each step represents one task, the next task might depend on it

            if one task fails, we halt for a bit and depending on task,
            we keep re-trying a designated previous task; or error out
        '''

        current_step = self.step

        print('Round starttime', isodate.today_minutes())
        print('---Step ' + str(current_step) + '---')
        print(self.STEP_DESC[current_step])

        match current_step:
            case 1:
                sleep.until_time_of_day(hour=self.fetch_hour, minute=self.fetch_minute)
                self.step = 2
            case 2:
                if self.nordpool.fetch():
                    self.step = 3
                else:
                    self.re_try = True; self.step = 2
            case 3:
                # if self.nordpool.confirm_date(isodate.today_plus_days(-3)):
                if self.nordpool.confirm_date('2023-01-23'):
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

        if not self.re_try:
            print('OK')
            return True

        # after x fresh restarts, exit -> this service needs attention/update
        if self.fresh_restarts > 5:
            print('to many fresh restarts, current step', current_step)
            print('Exit application')
            exit(1)

        # if a step has taken multiple re-tries, error out and start fresh
        if self.re_try_counter > 5:
            print('ERROR: starting fresh because step', current_step,'failed')
            self.step = 1
            self.re_try_counter = 0
            self.fresh_restarts += 1
            return False

        # if a step needs a re-try, halt until next 15 minute mark
        if self.re_try:
            print('step', current_step,'failed')
            print('halting for 15 minutes, then re-trying from step', self.step)
            sleep.until_next_quarter_hour()
            self.re_try = False
            self.re_try_counter += 1
            return False


def mainloop():
    app = Application()
    while 'I`m waiting for coffee':
        app.run()


mainloop()
