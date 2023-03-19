import asyncio

from cocuvida.timehandle import (timeofday, isodates, seconds)
from .generate import WorkerGenerate


async def generate_states():
    wg = WorkerGenerate()
    await wg.on_startup()
    # generate states for today
    await wg.generate_for_all_controlplans(isodates.today())
    while True:
        print(f'generate states loop start - time: {timeofday.now()}')
        if await wg.is_ready_to_generate_for_tomorrow():
            # generate states for tomorrow
            print(f'generate states for tomorrow - time: {timeofday.now()}')
            await wg.generate_for_all_controlplans(isodates.today_plus_days(1))

        # checks if new controlplan was added or old one was updated -> generate state for these
        await wg.generate_for_new_controlplans()
        sleep_time = seconds.until_next_minute()
        print(f'generate - sleep for {sleep_time} seconds')
        await asyncio.sleep(sleep_time)


async def publish_states():
    from cocuvida.sqldatabase import controlplans as sql_controlplans

    control_plans = await sql_controlplans.get_all_control_plans()
    for plan in control_plans:
        print(plan['name'])
    
    while True:
        print('publish_states')
        await asyncio.sleep(2)
        plans = await sql_controlplans.list_plan_names()
        for plan_name in plans:
            control_plan = await sql_controlplans.select_control_plan_by_plan_name(plan_name)
            print(plan_name)

'''  ---psudo-code---

    publish states
        1. for all device_types, load next state_value using state_timestamp from db.state_schedule
        2. check remaining time until state_timestamp
            if more than 10 minutes to next state
                jump back to step 1 in 10 minutes (maybe new states are recorded)
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