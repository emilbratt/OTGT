import asyncio

from cocuvida.timehandle import seconds

from .schedule import Schedule


async def run():
    schedule_obj = Schedule()
    while True:
        await schedule_obj.load_new_controlplans()
        await schedule_obj.publish_current_states()
        await schedule_obj.generate_states_for_tomorrow()
        #await schedule_obj.unload_controlplans()
        await asyncio.sleep(seconds.until_next_minute())
