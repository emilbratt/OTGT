from .GET import controller as get_controller
from .POST import controller as post_controller


async def loader(method: str) -> object:
    match method:
        case 'GET':
            return get_controller
        case 'POST':
            return post_controller
        case _:
            return None
