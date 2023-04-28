from cocuvida.web.views.home import View


async def controller(scope: dict, receive: object) -> View:
    view = View()
    await view.buttons()
    return view
