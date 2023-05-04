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

    # DATA FOR TABLE 1
    time_row = f'<td>{date} (hours)</td>'
    price_row = f'<td>{currency} {unit}</td>'
    percent_row = f'<td>Percent</td>'
    diff_factor_row = f'<td>Diff Factor</td>'
    weight_row = f'<td>Weight</td>'
    for element in elspot_data['prices']:
        if element['index'] % 4 == 0:
            h = element['time_start'][0:2]
            p = element['value']
            pr = element['percent']
            df = element['diff_factor']
            w = element['weight']
            time_row += f'<td>{h}</td>'
            price_row += f'<td>{p}</td>'
            percent_row += f'<td>{pr}%</td>'
            diff_factor_row += f'<td>{df}</td>'
            weight_row += f'<td>{w}</td>'

    # TABLE 1
    html += '<table style="width:100%">'
    html += f'<tr>{time_row}</tr>'
    html += f'<tr>{price_row}</tr>'
    html += f'<tr>{percent_row}</tr>'
    html += f'<tr>{diff_factor_row}</tr>'
    html += f'<tr>{weight_row}</tr>'
    html += f'</table>'

    # DATA FOR TABLE 2
    _max = elspot_data['max']
    spike = elspot_data['spike']
    slope = elspot_data['slope']
    _min = elspot_data['min']
    _avg = elspot_data['average']

    data_row = f'<td>Max: {_max}</td><td>Min: {_min}</td><td>Avg.: {_avg}</td><td>Slope: {slope}</td><td>Spike: {spike}</td>'
    # TABLE 2
    html += '<table style="width:25%">'
    html += f'<tr>{data_row}</tr>'
    html += f'</table>'
    html += '<br>'
    return html.encode()

async def state_schedule(state_schedule: list) -> bytes:
    if state_schedule == []:
        return b''
    html = str()
    controlplan = state_schedule[0][0]
    target = state_schedule[0][1]
    html += '<table style="width: 75%;">'
    html_header = f'<tr><th style="width: 25%;">Plan Name</th><th style="width: 20%;">Target Type</th><th style="width: 10%;">State</th><th style="width: 15%;">Status</th><th style="width: 20%;">Date</th><th style="width: 10%;">Time</th></tr>'
    html += html_header
    for row in state_schedule:
        # mark out controlplan and target_type with an extra header row when a new one appears for readabilty
        if controlplan != row[0] or target != row[1]:
            html += html_header
        controlplan = row[0]
        target = row[1]
        state = row[2]
        time_stamp = row[3]
        status_code = row[4]
        status_desc = STATUS_ENUMS[status_code]
        isodate = isodates.date_from_timestamp(time_stamp)
        time_of_day = isodates.time_from_timestamp(time_stamp)
        weekday = isodates.weekday_name_from_isodate(time_stamp)
        time_val = f'{weekday} - {time_stamp}'
        html += f'<tr><td>{controlplan}</td><td>{target}</td><td>{state}</td><td>{status_code} ({status_desc})</td><td>{weekday} - {isodate}</td><td>{time_of_day}</td></tr>'
    html += f'</table>'
    return html.encode()
