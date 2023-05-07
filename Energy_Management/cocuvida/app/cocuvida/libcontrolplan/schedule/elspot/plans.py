from . import libplans


async def generate(plan_name: str, plan_options: dict, elspot_data: dict) -> list:
    states = []
    match plan_name:
        case 'lowest_price_switch':
            states = await libplans.lowest_price_switch.generate(plan_options, elspot_data)
        case 'minimum_weight_level':
            states = await libplans.minimum_weight_level.generate(plan_options, elspot_data)
        case 'water_heater_switch':
            states = await libplans.water_heater_switch.generate(plan_options, elspot_data)
        case _:
            print(f'ERRPR: the elspot plan {plan_name} is not imlpemented')
    return states
