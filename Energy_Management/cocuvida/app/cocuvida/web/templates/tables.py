from cocuvida.sqldatabase.stateschedule import STATUS_ENUMS
from cocuvida.timehandle import isodates


async def elspot_processed(elspot_data: dict) -> bytes:
    # only show full hour prices for now (not quarterly) -> see if element['index'] % 4 == 0:
    if elspot_data == {}:
        return b''

    html = str()

    region = elspot_data['region']
    currency = elspot_data['currency']
    unit = elspot_data['unit']
    date = elspot_data['date']

    _max = elspot_data['max']
    spike = elspot_data['spike']
    slope = elspot_data['slope']
    _min = elspot_data['min']
    _avg = elspot_data['average']

    # BUILD STRUCTURE FOR HTML TABLE
    desc_table_data = f'<td>{region} {date} t.</td>'
    val_table_data = f'<td>{currency} {unit}</td>'
    for element in elspot_data['prices']:
        if element['index'] % 4 == 0:
            h = element['time_start'][0:2]
            p = element['value']
            desc_table_data += f'<td>{h}</td>'
            val_table_data += f'<td>{p}</td>'
    desc_table_data += '<td>|</td><td>Max</td><td>Min</td><td>Avg</td><td>|</td><td>Slope</td><td>Spike</td>'
    val_table_data += f'<td>|</td><td>{_max}</td><td>{_min}</td><td>{_avg}</td><td>|</td><td>{slope}</td><td>{spike}</td>'

    # HTML TABLE
    html += '<table style="width:100%">'
    html += f'<tr>{desc_table_data}</tr>'
    html += f'<tr>{val_table_data}</tr>'
    html += f'</table>'

    return html.encode()

async def state_schedule(state_schedule: list) -> bytes:
    if state_schedule == []:
        return b''
    name = state_schedule[0][0]
    target = state_schedule[0][1]
    html_header = f'<tr><th>Target Type</th><th>State</th><th>Status</th><th>Time</th></tr>'

    html = f'<p>Schedule: <strong>{name}</strong></p>'
    html += '<table style="width:75%">'
    html += html_header
    for row in state_schedule:
        # the list is sorted by target_type, so when a new one appears, we insert a header row in-between
        if target != row[1]:
            html += html_header

        target = row[1]
        state = row[2]
        time = row[3]
        weekday = isodates.weekday_name_from_isodate(time)
        time_val = f'{weekday} - {time}'
        status = STATUS_ENUMS[row[4]]
        html += f'<tr><td>{target}</td><td>{state}</td><td>{status}</td><td>{time_val}</td></tr>'
    html += f'</table>'
    return html.encode()
