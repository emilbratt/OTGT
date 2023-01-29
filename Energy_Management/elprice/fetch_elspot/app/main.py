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
        self.log = False
        self.nordpool = nordpooldayaheadinit(envar_get)
        self.http = httpdatastoreinit(envar_get)

        self.re_try = False
        self.re_try_counter = 0
        self.fresh_restarts = 0

        self.fetch_hour = int(envar_get('NORDPOOL_FETCH_HOUR'))
        self.fetch_minute = int(envar_get('NORDPOOL_FETCH_MINUTE'))

        a = self.http.raw_exists_on_datastore(isodate.today_plus_days(1))
        b = self.http.reshaped_exists_on_datastore(isodate.today_plus_days(1))
        c = timeofday.is_passed_time(hour=self.fetch_hour, minute=self.fetch_minute)
        if a and b and c:
            self.step = 1
        else:
            self.step = 2
        print('Application starttime:', isodate.today_minutes())
        print('Starting from step ' + str(self.step))

    def run(self) -> bool:
        '''
            each step represents one task, the next task might depend on it

            if one task fails then we halt for a bit before te-trying
            if the task depends on an earlier task, we re-try that task instead
            
            on to many re-tries, we error out and end the application with exit(1)
        '''

        current_step = self.step

        print('Round starttime:', isodate.today_seconds())
        print('---Step ' + str(current_step) + '---')
        print(self.STEP_DESC[current_step])

        match current_step:
            case 1:
                sleep.until_time_of_day(hour=self.fetch_hour, minute=self.fetch_minute)
                self.step = 2
            case 2:
                if self.nordpool.fetch_data(isodate.today_plus_days(1)):
                    self.step = 3
                else:
                    self.re_try = True; self.step = 2
            case 3:
                if self.nordpool.confirm_date():
                    self.step = 4
                else:
                    self.re_try = True; self.step = 2; self.log = self.nordpool.log
            case 4:
                if self.nordpool.confirm_currency():
                    self.step = 5
                else:
                    self.re_try = True; self.step = 2; self.log = self.nordpool.log
            case 5:
                if self.nordpool.confirm_unit():
                    self.step = 6
                else:
                    self.re_try = True; self.step = 2; self.log = self.nordpool.log
            case 6:
                if self.nordpool.reshape_data():
                    self.step = 7
                else:
                    self.re_try = True; self.step = 2; self.log = self.nordpool.log
            case 7:
                if self.http.send_raw(self.nordpool.data_raw):
                    self.step = 8
                else:
                    self.re_try = True; self.step = 7; self.log = self.http.log
            case 8:
                if self.http.send_reshaped(self.nordpool.data_reshaped):
                    self.step = 1
                else:
                    self.re_try = True; self.step = 8; self.log = self.http.log
            case _:
                print('some weird behavior occured, value for current_step =', current_step)
                exit(1)

        if not self.re_try:
            print('OK')
            return True

        # after x fresh restarts, exit -> this service needs attention/update
        if self.fresh_restarts > 3:
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
            print('---log---')
            print(self.log)
            print('App: halting for 15 minutes, then re-trying from step', self.step)
            sleep.until_next_quarter_hour()
            self.re_try = False
            self.re_try_counter += 1
            return False


def mainloop():
    sleep.seconds(3) # just to give the other services a head start
    app = Application()
    while 'I`m waiting for coffee':
        app.run()


mainloop()
