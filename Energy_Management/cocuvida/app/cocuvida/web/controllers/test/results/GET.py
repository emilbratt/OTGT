from urllib.parse import urlparse, parse_qs, unquote

from cocuvida.environment import env_var_get

from cocuvida.web.views.test import View

from .const import BUTTON_TEST_RESULTS

from . import controlplans, elspot


async def controller(scope: dict, receive: object) -> View:
    view = View()
    # only show this page if in testing environment
    if env_var_get('COCUVIDA_TESTING') != True:
        await view.not_testing_instance()
        return view

    await view.buttons(BUTTON_TEST_RESULTS)

    qs = scope['query_string']
    qs = unquote(qs)
    qs = parse_qs(qs, keep_blank_values=False, encoding='utf-8', separator='&')

    if 'testsite' not in qs:
        await view.title('Test results')
        return view

    site = qs.get('testsite')[0]
    match site:
        case 'elspot':
            view = await elspot.page(view, qs)
        case 'controlplans':
            view = await controlplans.page(view, qs)

    return view

