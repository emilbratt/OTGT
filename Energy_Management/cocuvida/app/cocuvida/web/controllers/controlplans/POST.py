import os

from cocuvida.authorize import check_secret
from cocuvida.web.views.controlplans import View
from cocuvida.web.formdata import FormDataParser


async def controller(scope: dict, receive: object):
    view = View()

    form_obj = FormDataParser(scope, receive)
    secret = await form_obj.load_string('secret')
    authorized = check_secret(secret)
    if not authorized:
        view.un_authorized()

    yaml_to_dict = await form_obj.load_yaml('controlplan')
    if yaml_to_dict == None:
        view.invalid_yaml()

    return view
