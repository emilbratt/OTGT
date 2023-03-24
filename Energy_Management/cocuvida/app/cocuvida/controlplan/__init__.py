from time import sleep
import asyncio

from cocuvida.timehandle import timeofday, isodates, seconds

from .generate import GenerateStates
from .publish import PublishStates


async def app():
    print('starting controlplan')
    genstates = GenerateStates()
    pubstates = PublishStates()

    await genstates.on_startup()
    await pubstates.on_startup()

    # generate states for today as first thing
    await genstates.generate_states_for_all_controlplans(isodates.today())

    while True:
        print(f'loop start: {timeofday.now()}')

        # if new controlplan was added or old one was updated -> generate states
        await genstates.generate_states_for_new_controlplans()
        # generate states for tomorrow if certain condition is met
        if await genstates.is_ready_to_generate_for_tomorrow():
            # generate states for tomorrow
            await genstates.generate_states_for_all_controlplans(isodates.today_plus_days(1))

        # periodically update controlplans and publish states for this time (HH:MM)
        await pubstates.update_controlplans()
        await pubstates.publish_current_states()

        sleep_time = seconds.until_next_minute()
        await asyncio.sleep(sleep_time)

def run_controlplan() -> None:
    asyncio.run(app())
