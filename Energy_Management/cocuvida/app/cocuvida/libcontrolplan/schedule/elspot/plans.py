from . import libplans


async def generate(elspot_plan: str, plan_options: dict, elspot_data: dict) -> list:
    states = []
    if not elspot_data['metadata']:
        # FIXME: implement adding state "inactive" as fallback if set in plan_options
        isodate = elspot_data['date']
        region = elspot_data['region']
        print(f'ERROR libcontrolplan.schedule.elspot.plans: can not generate schedule for {elspot_plan}')
        print(f'..data for {region} with date {isodate} has no metadata')
        return states

    match elspot_plan:
        case 'lowest_price_switch':
            states = await libplans.lowest_price_switch.generate(plan_options, elspot_data)
        case 'minimum_weight_level':
            states = await libplans.minimum_weight_level.generate(plan_options, elspot_data)
        case 'water_heater_switch':
            states = await libplans.water_heater_switch.generate(plan_options, elspot_data)
        case _:
            print(f'ERRPR: the elspot plan {elspot_plan} is not imlpemented')
    return states
