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
            iso_time_stamp = isodate + 'T' + row[0]
            device_type = row[1]
            state_val = row[2]
            states.append([device_type, iso_time_stamp, state_val])
        return states