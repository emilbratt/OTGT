async def vertical(rows: list) -> bytes:
    '''
        pass  [ [href, value], [href, value] ]
    '''
    html = '''
    <table>
    '''
    for row in rows:
        html += '<tr><td>'
        html += f'<button onclick="window.location.href=\'{row[0]}\';">{row[1]}</button>'
        html += '</td></tr>'
    html += '''
    </table>
    '''
    return html.encode()

async def horizontal(rows: list) -> bytes:
    '''
        pass  [ [href, value], [href, value] ]
    '''
    html = str()
    for row in rows:
        html += f'<button onclick="window.location.href=\'{row[0]}\';">{row[1]}</button>'
    return html.encode()
