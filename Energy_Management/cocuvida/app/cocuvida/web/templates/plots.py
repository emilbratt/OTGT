import base64


async def elspot(svg: str) -> bytes:
    svg_bytes = svg.encode()
    base64_svg = base64.b64encode(svg_bytes)
    html = f'<img src="data:image/svg+xml;base64,{base64_svg.decode()}" width="50%">'
    return html.encode()