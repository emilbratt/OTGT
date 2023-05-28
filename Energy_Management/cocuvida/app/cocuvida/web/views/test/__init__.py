from cocuvida.web.templates import buttons, forms, plots, tables


class View:

    HTML_START = b'''<!DOCTYPE html>\n<html>\n<head>
    <meta charset="UTF-8">
    <style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        text-align: center;
    }
    /*
    body {background-color: black;}
    p    {color: green;}
    */
    </style>
    '''

    HTML_HEAD_END = b'\n</head>'

    HTML_BODY_START = b'''\n<body>
    <button onclick="window.location.href='/';">Home</button>
    '''

    HTML_BODY_END = b'\n</body>\n</html>\n'

    def __init__(self):
        self.html_head = bytes()
        self.headers = {b'content-type': b'text/html'}
        self.html_title = b'<p>Cocuvida Test and Debugging</p><hr>'
        self.html_not_testing_env = bytes()
        self.html_paragraph = bytes()
        self.html_buttons = bytes()
        self.html_forms = bytes()
        self.html_plot = bytes()
        self.html_prices = bytes()
        self.html_state_schedule = bytes()
        self.http_code = 200

    async def title(self, title: str) -> None:
        self.html_title = f'<p>{title}</p><hr>'.encode()

    async def form_upload_elspot_dayahead(self) -> None:
        self.html_forms += await forms.upload_elspot_dayahead()

    async def form_select_elspot_dayahead(self) -> None:
        self.html_forms += await forms.select_elspot_dayahead()

    async def form_download_elspot_dayahead(self) -> None:
        self.html_forms += await forms.download_elspot_dayahead()

    async def not_testing_instance(self) -> None:
        self.http_code = 404
        self.html_not_testing_env += b'<p>This is not a testing environment</p>'

    async def buttons(self, shortcuts_list: list) -> None:
        self.html_buttons += await buttons.horizontal(shortcuts_list)
        self.html_buttons += b'<hr>'

    async def show_price(self, data: dict) -> None:
        self.html_prices += await tables.elspot_processed(data)

    async def show_plot(self, plot_svg: str) -> None:
        self.html_plot += await plots.elspot(plot_svg)

    async def show_state_schedule(self, rows: list) -> None:
        self.html_state_schedule += await tables.state_schedule(rows)

    async def add_paragraph(self, paragraph: str) -> None:
        self.html_paragraph += f'<p>{paragraph}</p>'.encode()

    async def send(self, send: object) -> None:
        headers = []
        for k,v in self.headers.items():
            headers.append([k,v])

        # SEND HTTP HEADER
        await send({
            'type': 'http.response.start',
            'status': self.http_code,
            'headers': headers,
        })

        # SEND HTTP BODY
        html_head_parts = [self.HTML_START + self.html_head + self.HTML_HEAD_END]
        for head in html_head_parts:
            await send({
                'type': 'http.response.body',
                'body': head,
                'more_body': True
            })
        await send({
            'type': 'http.response.body',
            'body': self.HTML_BODY_START,
            'more_body': True
        })
        html_body_parts = [
            self.html_title, self.html_buttons, self.html_not_testing_env,
            self.html_forms, self.html_paragraph, self.html_prices,
            self.html_plot, self.html_state_schedule
        ]
        for body in html_body_parts:
            await send({
                'type': 'http.response.body',
                'body': body,
                'more_body': True
            })
        await send({
            'type': 'http.response.body',
            'body': self.HTML_BODY_END,
            'more_body': False
        })
        return None
