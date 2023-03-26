from cocuvida.web.views.home import View


async def controller(scope: dict, receive: object):
    view = View()
    await view.overview()
    return view
