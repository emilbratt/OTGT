from time import sleep
import asyncio

from . import workers


async def app():
    asyncio.ensure_future(workers.generate_states())
    #asyncio.ensure_future(workers.publish_states())

def run_controlplan() -> None:
    print('starting controlplan')
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(app())
        loop.run_forever()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    finally:
        print('Closing Loop')
        loop.close()
