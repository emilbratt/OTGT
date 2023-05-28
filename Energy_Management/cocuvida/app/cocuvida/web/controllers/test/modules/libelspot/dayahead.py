from cocuvida import libelspot


async def download(currency: str) -> str:
    elspot_raw = await libelspot.download.download_dayahead(currency)
    return elspot_raw

async def process(view: object, elspot_raw: str):
    elspot_obj = libelspot.Elspot()
    elspot_processed = await elspot_obj.process_dayahead(elspot_raw)
    if not elspot_obj.process_ok:
        await view.add_paragraph('processing failed for elspot dayahead')
        return view

    for region, region_data in elspot_processed.items():
        if region_data['metadata']:
            await view.show_price(region_data)
            isodate = region_data['date']
            plot = await elspot_obj.plot_dayahead_date(region_data)
            if not elspot_obj.plot_ok:
                await view.add_paragraph(f'generating dayahead plot failed for {region} {isodate}')
                return view
            await view.show_plot(plot)

    return view
