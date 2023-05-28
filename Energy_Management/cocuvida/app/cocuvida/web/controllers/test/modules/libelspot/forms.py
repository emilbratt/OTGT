async def show(view: object):
    await view.form_download_elspot_dayahead()
    await view.form_select_elspot_dayahead()
    await view.form_upload_elspot_dayahead()
    return view
