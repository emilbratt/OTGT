from cocuvida.web.views.favicon import View


async def controller(scope: dict, receive: object) -> View:
    view = View()
    return view
