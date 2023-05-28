from cocuvida.environment import env_var_get
from cocuvida.sqldatabase import elspot as sql_elspot

from cocuvida.web.formdata import FormDataParser
from cocuvida.web.views.test import View

from . import dayahead, forms

async def controller(scope: dict, receive: object) -> View:
    view = View()
    if env_var_get('COCUVIDA_TESTING') != True:
        await view.not_testing_instance()
        return view

    await view.title('Test libelspot')
    form_obj = FormDataParser(scope, receive)
    submit_value =  await form_obj.load_string('submit')
    match submit_value:
        case 'upload_elspot_dayahead':
            new = True
            elspot_raw = await form_obj.load_string('elspot_dayahead_json')
            if elspot_raw == None:
                return view

        case 'select_elspot_dayahead':
            new = False
            isodate = await form_obj.load_string('elspot_dayahead_date')
            elspot_raw = await sql_elspot.select_elspot_raw_for_date(isodate)

        case 'download_elspot_dayahead':
            new = True
            currency = await form_obj.load_string('elspot_dayahead_currency')
            elspot_raw = await dayahead.download(currency)

        case _:
            view = await forms.show(view)
            return view

    if new:
        sql_result = await sql_elspot.insert_raw_elspot(elspot_raw)
        if not sql_result:
            await view.add_paragraph(f'SQL insert failed for elspot dayahead')

    view = await forms.show(view)
    view = await dayahead.process(view, elspot_raw)
    return view
