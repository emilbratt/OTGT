from urllib.parse import urlparse, urlencode

from cocuvida.environment import env_ini_get
from cocuvida.sqldatabase.elspot import (list_elspot_regions as sql_list_elspot_regions,
                                         select_region_elspot_data_for_date as sql_select_region_elspot_data_for_date)
from cocuvida.timehandle import isodates

from cocuvida.web.templates import buttons, tables


class View:

    HTML_START = b'''<!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    '''

    HTML_HEAD_END = b'''
    </head>
    '''

    HTML_STYLE = b'''
    <style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        text-align: center;
    }
    </style>
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
        self.html_title = b'<p>Elspot Prices</p><hr>'
        self.html_buttons = bytes()
        self.html_prices = bytes()
        self.http_code = 200

    async def list_elspot_regions(self):
        regions = await sql_list_elspot_regions()
        rows = []
        for region in regions:
            mapped = {'region': region}
            qs = urlencode(mapped)
            rows.append([f'/elspot/prices?{qs}', region])
        self.html_buttons = await buttons.horizontal(rows)
        self.html_buttons += b'<hr>'

    async def show_prices_for_today(self, region: str):
        elspot_data = await sql_select_region_elspot_data_for_date(region, isodates.today())
        self.html_prices += await tables.elspot_processed(elspot_data)

    async def show_plot_for_today(self, region: str):
        pass

    async def show_prices_for_time_window(self, region: str, time_from: str, time_to: str):
        pass

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
        html_head_parts = [self.HTML_START + self.html_head + self.HTML_HEAD_END + self.HTML_STYLE]
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
        html_body_parts = [self.html_title, self.html_buttons, self.html_prices]
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
