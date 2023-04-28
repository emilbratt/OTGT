from urllib.parse import urlparse, urlencode

from cocuvida.environment import env_ini_get
from cocuvida.sqldatabase import elspot as sql_elspot
from cocuvida.timehandle import isodates

from cocuvida.web.templates import buttons, tables, plots


class View:

    HTML_START = b'''<!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
    table, th, td {
        /* border: 1px solid white; */
        border: 1px solid black;
        border-collapse: collapse;
        text-align: center;
        /* color: green; */
    }
    /*
    body {background-color: black;}
    p    {color: green;}
    */
    </style>
    '''

    HTML_HEAD_END = b'''
    </head>
    '''

    HTML_BODY_START = b'''
    <body>
    <button onclick="window.location.href='/';">Home</button>
    '''

    HTML_BODY_END = b'''
    </body>
    </html>
    '''

    def __init__(self):
        self.html_head = bytes()
        self.headers = {b'content-type': b'text/html'}
        self.html_title = b'<p>Elspot</p><hr>'
        self.html_buttons = bytes()
        self.html_prices = bytes()
        self.html_plot = bytes()
        self.http_code = 200

    async def list_elspot_regions(self):
        regions = await sql_elspot.list_elspot_regions()
        rows = []
        for region in regions:
            mapped = {'region': region}
            qs = urlencode(mapped)
            rows.append([f'/elspot?{qs}', region])
        self.html_buttons = await buttons.horizontal(rows)
        self.html_buttons += b'<hr>'

    async def show_prices(self, region: str):
        elspot_data = await sql_elspot.select_processed_for_date_and_region(region, isodates.today())
        self.html_prices += await tables.elspot_processed(elspot_data)
        elspot_data = await sql_elspot.select_processed_for_date_and_region(region, isodates.today_plus_days(1))
        self.html_prices += await tables.elspot_processed(elspot_data)

    async def show_plot(self, region: str):
        plot_svg = await sql_elspot.select_plot_live_for_region(region)
        if plot_svg != '':
            self.html_plot += await plots.elspot(plot_svg)
        plot_svg = await sql_elspot.select_plot_for_date_and_region(region, isodates.today_plus_days(1))
        if plot_svg != '':
            self.html_plot += await plots.elspot(plot_svg)

    async def show_prices_for_time_window(self, region: str, time_from: str, time_to: str):
        raise Exception('MethodNotImplemented')

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
        html_body_parts = [self.html_title, self.html_buttons, self.html_prices, self.html_plot]
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
