# for errors or no content, refer to these controllers and use them here
from .controllers import method_not_allowed, page_not_found


async def route(scope: dict, receive: object, send: object) -> None:
    page = scope['path']

    # hard-coding imports..
    #   if switch case block grows to big (dont think the app will be that big)
    #   ..then I might implement dynamic import by name during runtime instead
    match page:
        case '/favicon.ico':
            from .controllers.favicon import loader
        case '/controlplans':
            from .controllers.controlplans import loader
        case '/plot':
            from .controllers.plot import loader
        case _:
            await page_not_found(scope, receive)
            return None

    # REQUEST METHOD NOT ALLOWED
    controller = await loader(scope['method'])
    if controller == None:
        await method_not_allowed(scope, receive)
        return None

    # IF REACHED THIS POINT, RUN REQEUST-METHOD FOR REQUEST
    view = await controller(scope, receive)
    await view.send(send)
