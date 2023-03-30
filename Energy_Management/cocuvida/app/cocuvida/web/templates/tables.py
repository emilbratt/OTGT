async def elspot_processed(elspot_data: dict) -> bytes:
    # only show full hour prices for now (not quarterly) -> see if element['index'] % 4 == 0:
    if elspot_data == {}:
        return b'N/A'
    html = str()
    region = elspot_data['region']
    currency = elspot_data['currency']
    unit = elspot_data['unit']
    date = elspot_data['date']
    _max = elspot_data['max']
    _min = elspot_data['min']
    _avg = elspot_data['average']
    html += f'<p>{region} Max: {_max} Min: {_min} Avg: {_avg}</p>'
    html += '<table style="width:100%">'
    time_row = f'<td>{date} t.</td>'
    price_row = f'<td>{currency} {unit}</td>'
    for element in elspot_data['prices']:
        if element['index'] % 4 == 0:
            h = element['time_start'][0:2]
            p = element['value']
            time_row += f'<td>{h}</td>'
            price_row += f'<td>{p}</td>'    
    html += f'<tr>{time_row}</tr>'
    html += f'<tr>{price_row}</tr>'
    html += f'</table>'
    return html.encode()
