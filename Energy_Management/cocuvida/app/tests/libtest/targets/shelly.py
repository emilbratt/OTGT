import aiohttp
import asyncio

from cocuvida.libcontrolplan.target.shelly import TargetShelly

from .const import SHELLY_TEST_STATE


async def publish_state(target_entry: dict) -> bool:
    '''
        target_entry for shelly
        {
            include_entry: bool
            user: <string>
            password: <string>
            entries:
                alias_for_device: ['ip/host', 'relay id']
                ...
                ...
        }
    
        will try to publish the state in SHELLY_TEST_STATE to all shellies listed in "entries"
    '''
    if not target_entry['include_entry']:
        return True

    async with aiohttp.ClientSession() as aiohttp_session:
        target_obj = TargetShelly(aiohttp_session)
        await target_obj.load_target_entry(target_entry)

        publish_tasks = []
        for alias in target_entry['entries']:
            task = target_obj.publish_state(alias, SHELLY_TEST_STATE)
            publish_tasks.append(task)

        results = await asyncio.gather(*publish_tasks,return_exceptions=True)
        for result in results:
            continue

    return True
