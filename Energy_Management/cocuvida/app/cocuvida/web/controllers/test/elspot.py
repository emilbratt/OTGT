from cocuvida.sqldatabase import elspot as sql_elspot

from .const import (
    TEST_DATES,
    GENERATED_PLOT_REGIONS,
    BUTTON_TEST_SITE_ELSPOT_REGION,
)

async def results(view: object, query_string: dict):
    await view.buttons(BUTTON_TEST_SITE_ELSPOT_REGION)
    if 'region' not in query_string.keys():
        return view

    paragraph = 'Only these regions have plots generated during testrun:'
    for region in GENERATED_PLOT_REGIONS:
        paragraph += f'<strong> {region}</strong>'
    await view.add_paragraph(paragraph)

    # test run only generates plots for these regions as of now
    region = query_string['region'][0]
    await view.add_paragraph(f'Test results for <strong>{region}</strong>')
    for isodate in TEST_DATES:
        data = await sql_elspot.select_processed_for_date_and_region(isodate, region)
        await view.show_price(data)
        if region in GENERATED_PLOT_REGIONS:
            plot = await sql_elspot.select_plot_for_date_and_region(isodate, region)
            if plot != '':
                await view.show_plot(plot)
    plot = await sql_elspot.select_plot_live_for_region(region)
    if plot != '':
        await view.show_plot(plot)

    return view
