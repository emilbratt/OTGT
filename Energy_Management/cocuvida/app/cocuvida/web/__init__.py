from cocuvida.environment import env_ini_get

from .routes import route


async def app(scope: dict, receive: object, send: object):
    try:
        path = scope['path']
    except KeyError:
        return None
    if scope['type'] != 'http':
        return None
    await route(scope, receive, send)

async def run_web():
    import uvicorn
    print('WEB START')
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
    await server.serve()
