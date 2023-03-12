from cocuvida.authorize import check_secret
from cocuvida.sqldatabase.controlplans import insert_control_plan
from cocuvida.sqldatabase.controlplans import delete_control_plan
from cocuvida.sqldatabase.controlplans import download_control_plan
from cocuvida.web.views.controlplans import View
from cocuvida.web.formdata import FormDataParser


async def controller(scope: dict, receive: object):
    view = View()
    form_obj = FormDataParser(scope, receive)
    secret = await form_obj.load_string('secret')
    authorized = check_secret(secret)
    if not authorized:
        await view.un_authorized()
        return view

    # HANDLE POST DATA
    operation =  await form_obj.load_string('submit')
    match operation:
        case 'upload':
            control_plan = await form_obj.load_string('control_plan')
            if control_plan != None:
                db_action_taken = await insert_control_plan(control_plan)
                await view.db_action(db_action_taken)

        case 'show' | 'download':
            plan_name = await form_obj.load_string('plan_name')
            if plan_name != None:
                control_plan_file = await download_control_plan(plan_name)
                if operation == 'show':
                    await view.show_control_plan_data(control_plan_file)
                elif operation == 'download':
                    await view.download_control_plan_data(control_plan_file)

        case 'delete':
            plan_name = await form_obj.load_string('plan_name')
            if plan_name != None:
                db_action_taken = await delete_control_plan(plan_name)
                await view.db_action(db_action_taken)

    await view.form_upload()
    await view.form_options()
    return view
