from . import libplans


async def generate(state_plan: str, plan_options: dict, elspot_data: dict) -> list:
    states = []
    match state_plan:
        case 'lowest_price_switch':
            states = await libplans.lowest_price_switch.generate(plan_options, elspot_data)
        case 'minimum_weight_level':
            states = await libplans.minimum_weight_level.generate(plan_options, elspot_data)
        case 'water_heater_switch':
            states = await libplans.water_heater_switch.generate(plan_options, elspot_data)
        case _:
            print(f'ERRPR: the elspot plan {state_plan} is not imlpemented')
    return states
