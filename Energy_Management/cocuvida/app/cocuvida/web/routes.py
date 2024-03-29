# for errors or no content, refer to these controllers and use them here
from .controllers import method_not_allowed, page_not_found


async def route(scope: dict, receive: object, send: object) -> None:
    route = scope['path']

    # hard-coding imports..
    #   if switch case block grows to big (dont think the app will be that big)
    #   ..then I might implement dynamic import by name during runtime instead
    match route:
        case '/':
            from .controllers.home import loader
        case '/controlplans':
            from .controllers.controlplans import loader
        case '/elspot':
            from .controllers.elspot import loader
        case '/favicon.ico':
            from .controllers.favicon import loader
        case '/plot':
            from .controllers.plot import loader
        case '/test':
            from .controllers.test import loader
        case '/test/results':
            from .controllers.test.results import loader
        case '/test/modules':
            from .controllers.test.modules import loader
        case '/test/modules/libelspot':
            from .controllers.test.modules.libelspot import loader
        case _:
            await page_not_found(send)
            return None

    # REQUEST METHOD NOT ALLOWED
    controller = await loader(scope['method'])
    if controller == None:
        await method_not_allowed(send)
        return None

    # IF REACHED THIS POINT, RUN REQEUST-METHOD FOR REQUEST
    view = await controller(scope, receive)
    await view.send(send)
