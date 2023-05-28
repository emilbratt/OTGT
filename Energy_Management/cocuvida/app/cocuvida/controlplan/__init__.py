import asyncio

from . import worker


async def app() -> None:
    print('CONTROLPLAN START')
    loop = asyncio.get_running_loop()
    loop.create_task(worker.run())

async def run_controlplan() -> None:
    await app()
