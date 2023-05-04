from cocuvida.timehandle import isodates


async def generate_states(schedule_time_entry: dict, isodate: str) -> list:
    states = []
    for row in schedule_time_entry['entries']:
        # iso_time_stamp evaluates to something like: 2023-06-02T17:30
        timeofday = row[0]
        state_time = f'{isodate} {timeofday}'
        target_type = row[1]
        state_value = row[2]
        states.append([target_type, state_value, state_time])
    return states
