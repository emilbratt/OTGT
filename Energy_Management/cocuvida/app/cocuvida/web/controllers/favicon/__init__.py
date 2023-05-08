from .GET import controller as get_controller


async def loader(method: str) -> object:
    match method:
        case 'GET':
            return get_controller
        case _:
            return None
