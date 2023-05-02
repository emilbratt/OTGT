from cocuvida.environment import env_var_get

from cocuvida.web.views.home import View

from .const import SHORTCUTS


async def controller(scope: dict, receive: object) -> View:
    view = View()
    await view.buttons(SHORTCUTS)
    if env_var_get('COCUVIDA_TESTING') == True:
        await view.buttons([['/test', 'Test-Results']])
    return view
