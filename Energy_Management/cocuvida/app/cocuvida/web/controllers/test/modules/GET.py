from cocuvida.environment import env_var_get

from cocuvida.web.views.test import View

from .const import BUTTON_TEST_MODULES


async def controller(scope: dict, receive: object) -> View:
    view = View()
    await view.title('Test modules')
    # only show this page if in testing environment
    if env_var_get('COCUVIDA_TESTING') != True:
        await view.not_testing_instance()
        return view

    await view.buttons(BUTTON_TEST_MODULES)
    return view
