import time

def temp_controlplan_parser(control_plan: dict):
    try:
        target = control_plan['target']
        calendar = control_plan['calendar']
        schedule = control_plan['schedule']
        return True
    except:
        return False

def run_controlplan():
    print('starting controlplans')
    while True:
        time.sleep(1)
