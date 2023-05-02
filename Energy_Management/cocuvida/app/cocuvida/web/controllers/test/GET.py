from urllib.parse import urlparse, parse_qs, unquote

from cocuvida.environment import env_var_get

from cocuvida.web.views.test import View

from .const import BUTTON_TEST_SITE_HOME


async def controller(scope: dict, receive: object) -> View:
    view = View()
    # only show this page if in testing environment
    if env_var_get('COCUVIDA_TESTING') != True:
        await view.not_testing_instance()
        return view

    qs = scope['query_string']
    qs = unquote(qs)
    qs = parse_qs(qs, keep_blank_values=False, encoding='utf-8', separator='&')

    await view.buttons(BUTTON_TEST_SITE_HOME)
    if 'testsite' not in qs:
        return view

    site = qs.get('testsite')[0]
    match site:
        case 'elspot':
            from .elspot import results
        case 'controlplans':
            from .controlplans import results

    view = await results(view, qs)
    return view

