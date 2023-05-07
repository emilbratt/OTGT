from cocuvida.timehandle import isodates


async def generate(plan_options: dict, elspot_data: dict) -> list:
    '''
        plan options are structured like:
        {
            below_price: only set states if prices is below, else use inactive state
            inactive_state: '<some_inactive_state>',
            weight_levels:
                0: '<some_state>'
                1: '<some_state>'
                2: '<some_state>'
                3: '<some_state>'
                4: '<some_state>'
                5: '<some_state>'
                6: '<some_state>'
                7: '<some_state>'
                8: null
                9: null
                10: null
        }

        weight_levels is used to define states based on weight level
        you can use the same state for multiple levels if need be
        setting the value to NULL will just force the use of the inactive_state

        NOTE:
            it is not guaranteed that weight levels less than 10 occours,
            as this is a matter of fluctuating prices..
            
            a flat price curve (all prices the same throughout the day),
            will all have weight levels = 10
    '''
    ISODATE = elspot_data['date']
    PRICE_THRESHOLD = int(plan_options['below_price'])

    # sort elspot prices based on weight level from lowest to highest
    sorted_price_array = sorted(elspot_data['prices'], key=lambda x: x['weight'], reverse=False)
    states = []

    for index in range(elspot_data['resolution']):
        # keep track on how many minutes have been recorded scheduled (also used to sort array back to time value)
        minute_index = sorted_price_array[index]['index'] * 15
        time_start = sorted_price_array[index]['time_start']
        state_timestamp = f'{ISODATE} {time_start}'
        price = sorted_price_array[index]['value']
        weight = sorted_price_array[index]['weight']
        if price >= PRICE_THRESHOLD:
            state = plan_options['inactive_state']
        elif price < PRICE_THRESHOLD:
            state = plan_options['weight_levels'][weight]
        states.append([minute_index, state, state_timestamp])

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
