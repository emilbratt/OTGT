async def loader(method: str) -> object:
    match method:
        case 'GET':
            from .GET import controller
        case 'POST':
            from .POST import controller
        case _:
            return None
    return controller
