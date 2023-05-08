from .target import TargetExampleTarget


# simple publish function that can be called without instanciating the target
async def publish_state(target_entry: dict, state_value: str) -> bool:
    '''
        this is just an example target, we always return True
        ..will however raise error if entry is not structured correctly
    '''
    for entry in target_entry['entries']:
        msg = ('key:', entry, 'Value:', target_entry['entries'][entry])
    return True
