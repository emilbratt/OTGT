from cocuvida.web.views.controlplans import View


async def controller(scope: dict, receive: object):
    view = View()
    return view
