import asyncio

from cocuvida.sqldatabase.controlplans import list_plan_names, get_control_plan


async def generate_states():
    '''
        psudo-code
        generate states for today if
            first run
            new control_plan is inserted
        generate states for tomorrow if
            states not generated AND
            (time is passed 14 OR elspot data exists)
    '''
    print('generate_states()')
    await asyncio.sleep(0)
    plans = await list_plan_names()
    for plan_name in plans:
        control_plan = await get_control_plan(plan_name[0])
        print(plan_name)


async def publish_states():
    '''
        psudo-code
        1. load next state_value using state_timestamp from db
        2. check remaining time until state_timestamp
            if more than 10 minutes to next state
                jump back to step 1 in 10 minutes (maybe new state are recorded)
            else:
                go to step 3
        3. sleep until time == state_timestamp
        4. load control_plan from table control_plans using plan_name
        5. publish states to all targets

        DB columns in state_schedule:
            plan_name
            state_value
            state_timestamp
    '''
    print('publish_states')
    await asyncio.sleep(0)
    plans = await list_plan_names()
    for plan_name in plans:
        control_plan = await get_control_plan(plan_name[0])
        print(plan_name)
