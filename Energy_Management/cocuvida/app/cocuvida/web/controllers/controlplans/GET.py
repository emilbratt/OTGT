from cocuvida.web.views.controlplans import View


async def controller(scope: dict, receive: object):
    view = View()
    view.form_upload_control_plan()
    return view
