from . import GET, POST

async def loader(method: str) -> object:
    match method:
        case 'GET':
            return GET.controller
        case 'POST':
            return POST.controller
        case _:
            return None
