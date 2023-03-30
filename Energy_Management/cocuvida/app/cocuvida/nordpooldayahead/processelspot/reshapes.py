
async def reshape_nok(elspot_raw: dict) -> list:
    # takes the raw elspot data and reshapes it into a list of each reaagion as key val arrays

    # extract all regions, as this is needed as first step
    regions = {}
    try:
        for row in elspot_raw['data']['Rows'][0]['Columns']:
            arr_scaffold = {
                'region': row['Name'],
                'date': elspot_raw['data']['DataStartdate'].split('T')[0],
                'currency': elspot_raw['currency'],
                'unit': 'ore/kWh',
                'max': False,
                'min': False,
                'average': False,
                'resolution': 0,
                'prices': []
            } # keep key-names like so, otherwise they will not match dataset
            region = row['Name']
            regions[region] = arr_scaffold
    except:
        return []
    # unpack data and assign to its correct region
    try:
        for row_number,row in enumerate(elspot_raw['data']['Rows']):
            start_hour = row['StartTime'].split('T')[1][:2]
            end_hour   = row['EndTime'].split('T')[1][:2]
            title_name = row['Name'] # avg, min or html special char for hour
            for col in elspot_raw['data']['Rows'][row_number]['Columns']:
                region = col['Name']
                value = col['Value']
                value = value.replace(' ', '')
                value = value.replace(',', '.')
                try:
                    value = float(value)
                    value = round(value*0.1)
                except ValueError:
                    if start_hour == '02':
                        # if this happens -> likely means moving from winter-time to summer-time at 2 AM
                        # ..and that means there wont be any values between 02:00 and 03:00 as this hour is skipped
                        continue
                if row['IsExtraRow']:
                    regions[region][title_name.lower()] = value
                elif not row['IsExtraRow']:
                    # here is also where the increase in resolution happens (hour 4x -> quarters)
                    for j in range(4):
                        # work out timestamp for each 15 minutes
                        start = str(start_hour) + ':' + str(j * 15).zfill(2)
                        if j == 3:
                            end = str(end_hour) + ':00'
                        else:
                            end = str(start_hour) + ':' + str((j+1) * 15).zfill(2)

                        # the current resolution value (incr. +1 each time, can be appended as index)
                        index = regions[region]['resolution']
                        price = {
                            'index': index,
                            'time_start': str(start),
                            'time_end': str(end),
                            'value': value
                        }
                        regions[region]['resolution'] += 1
                        regions[region]['prices'].append(price)

        # convert the data structure to the final one where each region (dict) is a list object
        data_reshaped = []
        for name in regions:
            # only append regions with values
            check_price = regions[name]['prices'][0]['value']
            if check_price != '-':
                data_reshaped.append( regions[name] )
        return data_reshaped
    except:
        return []
