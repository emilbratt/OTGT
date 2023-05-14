import asyncio

from . import worker


async def app():
    print('CONTROLPLAN START')
    asyncio.ensure_future(worker.run())

async def run_controlplan() -> None:
    await app()
