async def method_not_allowed(send: object):

    await send({
        'type': 'http.response.start',
        'status': 405,
        'headers': [
            [b'content-type', b'text/html'],
        ]
    })
    await send({
        'type': 'http.response.body',
        'body': '405 method not allowed'.encode(),

    })

async def page_not_found(send: object):
    await send({
        'type': 'http.response.start',
        'status': 404,
        'headers': [
            [b'content-type', b'text/html'],
        ]
    })
    await send({
        'type': 'http.response.body',
        'body': '404 not found'.encode(),
    })
