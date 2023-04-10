async def exampletarget_publish(target_entry: dict, state_value: str) -> bool:
    '''
        this is just an example target, we always return publish = True
    '''
    for entry in target_entry['entries']:
        msg = ('key:', entry, 'Value:', target_entry['entries'][entry])
        print('exampletarget publish', msg)
    return True
