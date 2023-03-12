from cocuvida.web.views.controlplans import View


async def controller(scope: dict, receive: object):
    view = View()
    await view.form_upload()
    await view.form_options()
    return view
