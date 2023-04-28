from cocuvida.authorize import check_secret
from cocuvida.sqldatabase.controlplans import (insert_control_plan, delete_control_plan)
from cocuvida.sqldatabase.stateschedule import delete_states_for_plan_name
from cocuvida.web.views.controlplans import View
from cocuvida.web.formdata import FormDataParser


async def controller(scope: dict, receive: object) -> View:
    view = View()
    form_obj = FormDataParser(scope, receive)
    secret = await form_obj.load_string('secret')
    authorized = check_secret(secret)
    if not authorized:
        await view.un_authorized()
        return view

    # HANDLE POST FORM-DATA
    submit_value =  await form_obj.load_string('submit')
    match submit_value:
        case 'upload':
            control_plan = await form_obj.load_string('control_plan')
            if control_plan == None:
                return view
            db_action_taken = await insert_control_plan(control_plan)
            await view.db_action(db_action_taken)

        case 'show':
            plan_name = await form_obj.load_string('plan_name')
            if plan_name != None:
                await view.show_control_plan_data(plan_name)

        case 'download':
            plan_name = await form_obj.load_string('plan_name')
            if plan_name != None:
                await view.download_control_plan_data(plan_name)

        case 'delete':
            plan_name = await form_obj.load_string('plan_name')
            if plan_name != None:
                # DELETE CONTROLPLAN
                db_action_taken = await delete_control_plan(plan_name)
                if db_action_taken == 'delete':
                    # DELETE STATE SCHEDULES
                    db_action_taken = await delete_states_for_plan_name(plan_name)
                await view.db_action(db_action_taken)

        case 'schedule':
            plan_name = await form_obj.load_string('plan_name')
            if plan_name != None:
                await view.show_state_schedule(plan_name)

    await view.form_upload()
    await view.form_options()
    return view
