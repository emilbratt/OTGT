from cocuvida.environment import env_var_get

from cocuvida.web.views.test import View

from . import forms

async def controller(scope: dict, receive: object) -> View:
    view = View()
    if env_var_get('COCUVIDA_TESTING') != True:
        await view.not_testing_instance()
        return view

    await view.title('Test libelspot')
    view = await forms.show(view)
    return view
