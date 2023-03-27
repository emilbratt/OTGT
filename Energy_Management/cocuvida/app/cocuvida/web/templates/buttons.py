async def vertical(rows: list) -> bytes:
    html = b'''
    <table>
    '''
    for row in rows:
        html += b'<tr><td>'
        html += f'<button onclick="window.location.href=\'{row[0]}\';">{row[1]}</button>'.encode()
        html += b'<tr><td>'
    html += b'''
    </table>
    '''
    return html
