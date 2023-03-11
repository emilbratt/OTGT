from cocuvida.authorize import check_secret
from cocuvida.sqldatabase.controlplans import insert_control_plan
from cocuvida.web.views.controlplans import View
from cocuvida.web.formdata import FormDataParser


async def controller(scope: dict, receive: object):
    view = View()
    view.form_upload_control_plan()

    form_obj = FormDataParser(scope, receive)
    secret = await form_obj.load_string('secret')
    authorized = check_secret(secret)
    if not authorized:
        view.un_authorized()
        return view

    control_plan = await form_obj.load_yaml('controlplan')
    if control_plan == None:
        view.invalid_yaml()
        return view

    action = await insert_control_plan(control_plan)
    view.db_action(action)

    return view
