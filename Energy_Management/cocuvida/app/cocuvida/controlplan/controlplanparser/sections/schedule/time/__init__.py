from cocuvida.timehandle import isodates


class Entry:
    '''
        entry for processing sub entries found below in controlplan
        schedule -> time -> include_entry: true
    '''

    def __init__(self, time: dict):
        self.t = time

    async def generate_states(self, isodate: str) -> list:
        states = []
        for row in self.t['entries']:
            # iso_time_stamp evaluates to something like: 2023-06-02T17:30
            timeofday = row[0]
            state_time = f'{isodate} {timeofday}'
            target_type = row[1]
            state_value = row[2]
            states.append([target_type, state_value, state_time])
        return states
