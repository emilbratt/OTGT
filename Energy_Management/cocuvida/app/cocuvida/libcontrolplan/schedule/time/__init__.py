async def generate_states(schedule_time_entry: dict, isodate: str) -> list:
    states = []
    for target, entries in schedule_time_entry.items():
        for row in entries:
            timeofday = row[0]
            state_value = row[1]
            target_type = target
            state_timestamp = f'{isodate} {timeofday}'
            states.append([target_type, state_value, state_timestamp])
    return states
