async def mqtt_publish(target_entry: dict, state_value: str) -> bool:
    for entry in target_entry['entries']:
        print('mqtt publish ref', entry)
        msg = ('key:', entry, 'Value:', target_entry['entries'][entry])
    return True
