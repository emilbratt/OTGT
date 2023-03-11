async def loader(method: str):
    match method:
        case 'GET':
            from .GET import controller
        case _:
            return None
    return controller
