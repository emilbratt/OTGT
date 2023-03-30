from cocuvida.timehandle import isodates

STATE_ENUMS = ['not published', 'published', 'target disabled', 'publish failed']


async def elspot_processed(elspot_data: dict) -> bytes:
    # only show full hour prices for now (not quarterly) -> see if element['index'] % 4 == 0:
    if elspot_data == {}:
        return b''

    html = str()
    region = elspot_data['region']
    currency = elspot_data['currency']
    unit = elspot_data['unit']
    date = elspot_data['date']

    html += '<table style="width:75%">'
    time_row = f'<td>{region} {date} t.</td>'
    price_row = f'<td>{currency} {unit}</td>'
    for element in elspot_data['prices']:
        if element['index'] % 4 == 0:
            h = element['time_start'][0:2]
            p = element['value']
            time_row += f'<td>{h}</td>'
            price_row += f'<td>{p}</td>'    
    html += f'<tr>{time_row}</tr>'
    html += f'<tr>{price_row}</tr>'
    _max = elspot_data['max']
    spike = elspot_data['spike']
    slope = elspot_data['slope']
    _min = elspot_data['min']
    _avg = elspot_data['average']
    html += f'</table>'

    html += '<table style="width:25%">'
    html += '<tr>'
    html += '<td>Max</td><td>Min</td><td>Avg</td><td>Slope</td><td>Spike</td>'
    html += '</tr>'
    html += '<tr>'
    html += f'<td>{_max} {unit}</td><td>{_min} {unit}</td><td>{_avg} {unit}</td><td>{slope}</td><td>{spike}</td>'
    html += '</tr>'
    html += '</table>'

    return html.encode()

async def state_schedule(state_schedule: list) -> bytes:
    if state_schedule == []:
        return b''
    name = state_schedule[0][0]
    target = state_schedule[0][1]
    html_header = f'<tr><th>Target Type</th><th>State</th><th>Status</th><th>Time</th></tr>'

    html = f'<p>{name} from today -></p>'
    html += '<table style="width:75%">'
    html += html_header
    for row in state_schedule:
        # the list is sorted by target_type, so when a new one appears, we insert header row in-between
        if target != row[1]:
            html += html_header

        target = row[1]
        state = row[2]
        time = row[3]
        weekday = isodates.weekday_name_from_isodate(time)
        time_val = f'{weekday} - {time}'
        status = STATE_ENUMS[row[4]]
        html += f'<tr><td>{target}</td><td>{state}</td><td>{status}</td><td>{time_val}</td></tr>'
    html += f'</table>'
    return html.encode()
