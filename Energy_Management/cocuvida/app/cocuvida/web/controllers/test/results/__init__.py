from . import GET


async def loader(method: str) -> object:
    match method:
        case 'GET':
            return GET.controller
        case _:
            return None
