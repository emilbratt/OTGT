from time import sleep
import asyncio
from .workers import generate_states, publish_states



async def app():
    asyncio.ensure_future(generate_states())
    asyncio.ensure_future(publish_states())

    # await generate_states()
    # await publish_states()

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

    #asyncio.run(app())
