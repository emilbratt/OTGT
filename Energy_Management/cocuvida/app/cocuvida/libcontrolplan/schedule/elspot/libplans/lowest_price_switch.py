from cocuvida.timehandle import isodates


async def generate(plan_options: dict, elspot_data: dict) -> list:
    '''
        plan options are structured like:
        {
            operation_time: minutes,
            active_state: state,
            inactive_state: state
        }
    '''
    ISODATE = elspot_data['date']
    OPERATION_TIME = int(plan_options['operation_time'])
    all_indexes = elspot_data['resolution']
    operation_indexs = OPERATION_TIME // 15
    non_operating_indexes = all_indexes - operation_indexs
    remaining_minutes = OPERATION_TIME % 15
    
    # sort elspot price data based on the price from lowest to highest
    sorted_price_array = sorted(elspot_data['prices'], key=lambda x: x['value'], reverse=False)
    states = []
    # append all the active states first, as they fit with the lowest prices, then the inactive ones
    for index in range(elspot_data['resolution']):
        timeofday = sorted_price_array[index]['time_start']
        state_timestamp = f'{ISODATE} {timeofday}'
        # keep track on how many minutes from 00:00 until 23:59 has been recorded (also used to sort array)
        minute_index = sorted_price_array[index]['index'] * 15

        if index < operation_indexs:
            states.append([minute_index, plan_options['active_state'], state_timestamp])
        elif index == operation_indexs:
            states.append([minute_index, plan_options['active_state'], state_timestamp])
            end = isodates.add_minutes_to_timestamp(state_timestamp, remaining_minutes)
            states.append([minute_index+remaining_minutes, plan_options['inactive_state'], end])
        elif index > operation_indexs:
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