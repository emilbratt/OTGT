import asyncio

from .target import TargetMQTT


# simple publish function that can be called
async def publish_state(target_entry: dict, state_value: str) -> bool:
    if not target_entry['include_entry']:
        return True
    if state_value not in target_entry['states']:
        print(f'ERROR: mqtt state {state_value} does not exist')
        return False

    res = True
    target_obj = TargetMQTT()
    await target_obj.load_target_entry(target_entry)
    publish_tasks = []
    for alias in target_entry['entries']:
        task = target_obj.publish_state(alias, state_value)
        publish_tasks.append(task)
    results = await asyncio.gather(*publish_tasks, return_exceptions=True)
    for result in results:
        if not result:
            res = False

    return res
