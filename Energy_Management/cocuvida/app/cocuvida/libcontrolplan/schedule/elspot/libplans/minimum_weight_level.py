WEIGHT_LEVELS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


async def generate(plan_options: dict, elspot_data: dict) -> list:
    '''
        this plan can be ideal for use with charging a battery cluster or a car
        it is not certain that it will operate, unless you set a farily high price_threshold

        plan options are structured like:
        {
            price_threshold: price
            inactive_state: state
            weight_levels: [
                state,
                state,
                state,
                state,
                ..
                state
            ]
        }
        weight_levels contains a list of up to (including) 10 states
        the states can differ
    '''

    states = []
    # isodate = elspot_data['date']
    # price_array = elspot_data['prices']
    # OPERATION_TIME = int(plan_options['operation_time']) # in minutes
    # ACTIVE_STATE = plan_options['active_state']
    # INACTIVE_STATE = plan_options['inactive_state']
    # index_list = [x['index'] for x in elspot_data['prices']]
    # operations_minutes = 0
    # used_indexes = []
    # for target_weight in WEIGHT_LEVELS:
    #     for index in index_list:
    #         if index not in used_indexes:
    #             weight = price_array[index]['weight']
    #             timeofday = price_array[index]['time_start']
    #             state_timestamp = f'{isodate} {timeofday}'
    #             if weight == target_weight:
    #                 state = ACTIVE_STATE
    #                 states.append([state, state_timestamp])
    #                 used_indexes.append(index)
    #                 operations_minutes += 15
    #             if operations_minutes >= OPERATION_TIME:
    #                 return states
    return states
