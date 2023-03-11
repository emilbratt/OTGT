import uvicorn

from cocuvida.environment import env_ini_get

from .routes import route


# this is the entrypoint for uvicorn when called on startup
async def app(scope: dict, receive: object, send: object):
    try:
        path = scope['path']
    except KeyError:
        return None
    if scope['type'] != 'http':
        return None
    await route(scope, receive, send)


# the function to call if starting uvicorn via script (not via cli)
def run_web():
    print('starting web')
    port = env_ini_get('cocuvida', 'port')
    config = uvicorn.Config(
        'cocuvida.web:app',
        host='0.0.0.0',
        port=int(port),
        log_level='info',
        use_colors=True,
        loop='asyncio',
    )
    server = uvicorn.Server(config)
    server.run()
