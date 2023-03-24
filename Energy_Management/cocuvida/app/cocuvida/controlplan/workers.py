import asyncio

from cocuvida.timehandle import timeofday, isodates, seconds
from .generate import WorkerGenerate
from .publish import WorkerPublish


async def generate_states():
    wgen = WorkerGenerate()
    await wgen.on_startup()
    # generate states for today
    await wgen.generate_for_all_controlplans(isodates.today())
    while True:
        print(f'GENERATE LOOP: {timeofday.now()}')
        # if new controlplan was added or old one was updated -> generate states
        await wgen.generate_for_new_controlplans()
        # generate states for tomorrow if certain condition is met
        if await wgen.is_ready_to_generate_for_tomorrow():
            # generate states for tomorrow
            await wgen.generate_for_all_controlplans(isodates.today_plus_days(1))

        sleep_time = seconds.until_next_minute()
        await asyncio.sleep(sleep_time)

async def publish_states():
    wpub = WorkerPublish()
    await wpub.on_startup()

    while True:
        print(f'PUBLISH LOOP: {timeofday.now()}')
        await wpub.update_controlplans()
        await wpub.publish_current_states()

        sleep_time = seconds.until_next_minute()
        await asyncio.sleep(sleep_time)