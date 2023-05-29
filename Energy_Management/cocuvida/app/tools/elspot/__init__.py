import asyncio

from cocuvida import libelspot

from . import const, dayahead


def show(file_ref: str, region: str):
    elspot_obj = libelspot.Elspot()
    processed_elspot = None
    with open(const.FILES[file_ref]) as f:
        raw_elspot = f.read()
        processed_elspot = asyncio.run(elspot_obj.process_dayahead(raw_elspot))
    title = f'Elspot Visualizer for {region}'
    break_line = str()
    for _ in title:
        break_line += '-'
    print(f'{title}\n{break_line}\n')
    dayahead.vertical_curve(processed_elspot[region])
    dayahead.horizontal_curve(processed_elspot[region])
    dayahead.overview(processed_elspot[region])
