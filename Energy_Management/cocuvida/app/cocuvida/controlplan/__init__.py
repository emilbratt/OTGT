from time import sleep
import asyncio
from .states import generate_states, publish_states


async def app():
    await generate_states()
    await publish_states()

def run_controlplan() -> None:
    print('starting controlplan')
    asyncio.run(app())
