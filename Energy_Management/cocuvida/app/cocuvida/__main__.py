import sys
import threading

from cocuvida.sqldatabase import scripts
from cocuvida.web import run_web
from cocuvida.controlplans import run_controlplans


def init():
    scripts.run('create_tables.sql')

def main() -> int:
    init()
    arg = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]

    # run selected service or run all as threads
    match arg:
        case 'web':
            run_web()
        case 'controlplans':
            run_controlplans()
        case _:
            uvc = threading.Thread(target=run_web, daemon=True)
            cpl = threading.Thread(target=run_controlplans, daemon=True)
            uvc.start()
            cpl.start()
            uvc.join()
            cpl.join()

    return 0


if __name__ == '__main__':
    sys.exit(main())
