import aiohttp
import asyncio

from .const import SUPPORTED_STATES
from .target import TargetShelly


# simple publish function that can be called
async def publish_state(target_entry: dict, state_value: str) -> bool:
    if not target_entry['include_entry']:
        return True
    if state_value not in SUPPORTED_STATES:
        print(f'ERROR: {state_value} is not a supported state')
        return False

    res = True
    publish_tasks = []
    async with aiohttp.ClientSession() as aiohttp_session:
        target_obj = TargetShelly(aiohttp_session)
        await target_obj.load_target_entry(target_entry)
        for alias in target_entry['entries']:
            task = target_obj.publish_state(alias, state_value)
            publish_tasks.append(task)
        results = await asyncio.gather(*publish_tasks, return_exceptions=True)
        for result in results:
            if not result:
                res = False

        await target_obj.close()
        return res
