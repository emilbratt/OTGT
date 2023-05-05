async def generate_states(schedule_time_entry: dict, isodate: str) -> list:
    states = []
    for row in schedule_time_entry['entries']:
        timeofday = row[0]
        target_type = row[1]
        state_value = row[2]
        state_timestamp = f'{isodate} {timeofday}'
        states.append([target_type, state_value, state_timestamp])
    return states
