from cocuvida.timehandle import isodates


class WorkerPublish:
    '''
        load states from SQL table state_schedule and publish
    '''
    def __init__(self):
        self.init_time = isodates.timestamp_now()
        self.on_startup_ok = False
        self.date_today = None

    async def on_startup(self) -> None:
        self.date_today = isodates.today()
        self.on_startup_ok = True

    async def is_next_day(self) -> None:
        if not self.on_startup_ok:
            raise Exception('OnStartupError: run WorkerGenerate.on_startup() before anything else')

        if self.date_today == isodates.today():
            return False
        self.date_today = isodates.today()
        return True