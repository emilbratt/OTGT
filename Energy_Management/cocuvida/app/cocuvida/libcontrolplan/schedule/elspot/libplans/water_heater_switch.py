from cocuvida.timehandle import isodates


async def generate(plan_options: dict, elspot_data: dict) -> list:
    '''
        plan options
        {
            operation_time: <n_minutes>,
            active_state: <state>,
            inactive_state: <state>
        }
        active at least 60 minutes in each quarter of the day
        where each part is split up on these hours
            00:00 - 06:00
            06:00 - 12:00
            12:00 - 18:00
            18:00 - 00:00
    '''
    ISODATE = elspot_data['date']
    OPERATION_TIME = int(plan_options['operation_time'])
    if OPERATION_TIME < 240:
        print('ERROR: operation time must be greater or equal to 240 which equal 4 hours, one for each part of the day')
        return []
    OPERATION_INDEXS = OPERATION_TIME // 15 # one for each 15 minutes
    REMAINING_MINUTES = OPERATION_TIME % 15 # remaining minutes

    # split price array into 4 arrays
    arr_a = [] # first quarter of day
    arr_b = [] # second quarter of day
    arr_c = [] # third quarter of day
    arr_d = [] # last quarter of day
    split_val_a = elspot_data['resolution'] // 4
    split_val_b = split_val_a * 2
    split_val_c = split_val_a * 3
    for entry in elspot_data['prices']:
        index = entry['index']
        if index < split_val_a:
            arr_a.append(entry)
        elif index < split_val_b:
            arr_b.append(entry)
        elif index < split_val_c:
            arr_c.append(entry)
        else:
            arr_d.append(entry)

    states = []

    # ADD AT LEAST 60 MINUTES FOR EACH 4 PARTS OF THE DAY
    # sort elspot prices for each array based on price from lowest to highest
    arr_a_sorted = sorted(arr_a, key=lambda x: x['value'], reverse=False)
    arr_b_sorted = sorted(arr_b, key=lambda x: x['value'], reverse=False)
    arr_c_sorted = sorted(arr_c, key=lambda x: x['value'], reverse=False)
    arr_d_sorted = sorted(arr_d, key=lambda x: x['value'], reverse=False)
    # merge all 4 arrays into a zip object making it easy to iterat eall 4 at once
    all_arrs = zip(arr_a_sorted, arr_b_sorted, arr_c_sorted, arr_d_sorted)
    remaining_entries = []
    used_indexes = 0
    for tuple_arr in all_arrs:
        if used_indexes < 16:
            for i in range(4):
                used_indexes += 1
                timeofday = tuple_arr[i]['time_start']
                minute_index = tuple_arr[i]['index'] * 15
                state_timestamp = f'{ISODATE} {timeofday}'
                states.append([minute_index, plan_options['active_state'], state_timestamp])
        else:
            remaining_entries.append(tuple_arr[0])
            remaining_entries.append(tuple_arr[1])
            remaining_entries.append(tuple_arr[2])
            remaining_entries.append(tuple_arr[3])

    # ADD THE REST OF THE STATES FOR ALL THE LOWEST REMAINING TIMES OF DAY
    remaining_entries = sorted(remaining_entries, key=lambda x: x['value'], reverse=False)
    for index in range(elspot_data['resolution'] - used_indexes):
        timeofday = remaining_entries[index]['time_start']
        state_timestamp = f'{ISODATE} {timeofday}'
        minute_index = remaining_entries[index]['index'] * 15
        total_used = index + used_indexes
        if total_used < OPERATION_INDEXS:
            states.append([minute_index, plan_options['active_state'], state_timestamp])
        elif total_used == OPERATION_INDEXS:
            states.append([minute_index, plan_options['active_state'], state_timestamp])
            end = isodates.add_minutes_to_timestamp(state_timestamp, REMAINING_MINUTES)
            states.append([minute_index+REMAINING_MINUTES, plan_options['inactive_state'], end])
        elif total_used > OPERATION_INDEXS:
            states.append([minute_index, plan_options['inactive_state'], state_timestamp])

    # using the minute_index to order the states by time
    sorted_states = sorted(states, key=lambda x: x[0], reverse=False)
    cleaned_states = []
    state = sorted_states[0][1]
    timestamp = sorted_states[0][2]
    cleaned_states.append([state, timestamp])
    # for every record where the same states appear, remove the trailing one (no need to call the same state if already called)
    for index in range(1, elspot_data['resolution']):
        state = sorted_states[index][1]
        previous_state = sorted_states[index-1][1]
        if state != previous_state:
            timestamp = sorted_states[index][2]
            cleaned_states.append([state, timestamp])
    return cleaned_states
