import asyncio
import sys

from cocuvida.elspot import run_elspot
from cocuvida.controlplan import run_controlplan
from cocuvida.web import run_web
from cocuvida.sqldatabase import scripts

SERVICES = {
    'web': 'uvicorn web service',
    'elspot': 'elspot service',
    'controlplan': 'controlplan service',
    'all': 'all of the above',
}


def init_database() -> None :
    scripts.run('create_tables.sql')

def list_services(service: str) -> None:
    print(f'{service} is not a recognised service')
    print('Listing valid arguments and the service description')
    for k,v in SERVICES.items():
        print(f'{k}\n\t..{v}\n')

def main() -> int:
    service = 'all'
    if len(sys.argv) > 1:
        service = sys.argv[1]

    init_database()

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        match service:
            case 'controlplan':
                loop.create_task(run_controlplan())
            case 'elspot':
                loop.create_task(run_elspot())
            case 'web':
                loop.create_task(run_web())
            case 'all':
                loop.create_task(run_controlplan())
                loop.create_task(run_elspot())
                loop.create_task(run_web())
            case _:
                list_services(service)
                return 1
        loop.run_forever()
    finally:
        loop.close()
        return 0

if __name__ == '__main__':
    sys.exit(main())
