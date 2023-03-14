import sys
import threading

from cocuvida.sqldatabase import scripts
from cocuvida.web import run_web
from cocuvida.controlplan import run_controlplan
from cocuvida.elspot import run_elspot


def init():
    scripts.run('create_tables.sql')

def main() -> int:
    init()
    arg = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]

    # run selected service or run all
    match arg:
        case 'web':
            run_web()
        case 'elspot':
            run_elspot()
        case 'controlplan':
            run_controlplan()
        case _:
            uvc = threading.Thread(target=run_web, daemon=True)
            cpl = threading.Thread(target=run_controlplan, daemon=True)
            els = threading.Thread(target=run_elspot, daemon=True)
            uvc.start()
            cpl.start()
            els.start()
            uvc.join()
            cpl.join()
            els.join()

    return 0


if __name__ == '__main__':
    sys.exit(main())
