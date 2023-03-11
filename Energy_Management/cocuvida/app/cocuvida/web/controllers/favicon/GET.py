from cocuvida.web.views.favicon import View


async def controller(scope: dict, receive: object):
    view = View()
    return view
