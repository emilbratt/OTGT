from cocuvida.environment import env_var_get

from cocuvida.web.views.home import View

from .const import PAGES, DEBUG_PAGES


async def controller(scope: dict, receive: object) -> View:
    view = View()
    await view.buttons(PAGES)
    if env_var_get('COCUVIDA_TESTING') == True:
        await view.buttons(DEBUG_PAGES)
    return view
