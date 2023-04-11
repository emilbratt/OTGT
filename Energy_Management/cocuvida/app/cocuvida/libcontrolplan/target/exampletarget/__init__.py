async def exampletarget_publish(target_entry: dict, state_value: str) -> bool:
    '''
        this is just an example target, we always return True
        ..will however raise error if entries are not correct
    '''
    for entry in target_entry['entries']:
        msg = ('key:', entry, 'Value:', target_entry['entries'][entry])
    return True
