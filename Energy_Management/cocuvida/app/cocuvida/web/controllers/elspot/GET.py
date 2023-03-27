from cocuvida.web.views.elspot import View


async def controller(scope: dict, receive: object):
    view = View()
    await view.buttons()
    return view
