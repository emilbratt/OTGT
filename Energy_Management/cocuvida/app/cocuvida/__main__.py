import sys
import threading

from cocuvida.sqldatabase import scripts
from cocuvida.web import run_web
from cocuvida.controlplan import run_controlplan
from cocuvida.elspot import run_elspot


SERVICES = {
    'web': 'start uvicorn web backend',
    'elspot': 'start elspot download and process daempon',
    'controlplan': 'start controlplan process daemon',
    'all': 'start all the above',
}

def init() -> None :
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

    init()

    # run selected service or run all
    match service:
        case 'web':
            run_web()
        case 'elspot':
            run_elspot()
        case 'controlplan':
            run_controlplan()
        case 'all':
            uvc = threading.Thread(target=run_web, daemon=True)
            cpl = threading.Thread(target=run_controlplan, daemon=True)
            els = threading.Thread(target=run_elspot, daemon=True)
            uvc.start()
            cpl.start()
            els.start()
            uvc.join()
            cpl.join()
            els.join()
        case _:
            list_services(service)
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
