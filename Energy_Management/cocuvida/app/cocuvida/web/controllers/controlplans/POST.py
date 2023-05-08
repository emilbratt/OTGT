from cocuvida.authorize import check_secret
from cocuvida.sqldatabase import controlplans as sql_controlplans
from cocuvida.sqldatabase import stateschedule as sql_stateschedule

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
            db_action_taken = await sql_controlplans.insert_control_plan(control_plan)
            await view.db_action(db_action_taken)

        case 'show':
            plan_name = await form_obj.load_string('plan_name')
            if plan_name != None:
                plan_data = await sql_controlplans.get_stringio_control_plan_by_name(plan_name)
                await view.show_control_plan_data(plan_data)

        case 'download':
            plan_name = await form_obj.load_string('plan_name')
            if plan_name != None:
                plan_data = await sql_controlplans.get_stringio_control_plan_by_name(plan_name)
                await view.download_control_plan_data(plan_data)

        case 'delete':
            plan_name = await form_obj.load_string('plan_name')
            if plan_name != None:
                # DELETE CONTROLPLAN
                db_action_taken = await sql_controlplans.delete_control_plan(plan_name)
                if db_action_taken == 'delete':
                    # DELETE STATE SCHEDULES
                    db_action_taken = await sql_stateschedule.delete_states_for_plan_name(plan_name)
                await view.db_action(db_action_taken)

        case 'schedule':
            plan_name = await form_obj.load_string('plan_name')
            if plan_name != None:
                shcedule = await sql_stateschedule.select_all_states_today_for_plan_name(plan_name)
                await view.show_state_schedule(shcedule)

    await view.form_upload()
    await view.form_options()
    return view
