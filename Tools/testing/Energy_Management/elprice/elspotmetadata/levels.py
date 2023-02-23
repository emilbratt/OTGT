def percent_of_max(arr: list) -> list:
    '''
        min price = 0%
        max price = 100%
        other prices = between 0% and 100%
    '''
    ret_data = []
    _max_ = max(arr)
    _min_ = min(arr)
    resolution = len(arr)
    for index in range(resolution):
        price = arr[index]
        if price == _max_:
            percent = 100
        elif price == _max_:
            percent = 0
        else:
            try:
                percent = round( (price-_min_) * (100 / (_max_-_min_)) )
            except ZeroDivisionError:
                percent = 100
        ret_data.append(percent)
    return ret_data

def weight_range(arr: list) -> list:
    '''
        max price weight = 10 
        min price weight = 0

        high fluctuation -> weights spread out between 0 and 10
        low fluctuation  -> many weights close to 10
        flat price curve -> all weights will be 10

        quick summary
            weight =  2.5 ->  price =   25% of max price
            weight =  5   ->  price =   50% of max price
            weight =  7.5 ->  price =   75% of max price

    '''
    ret_data = []
    _max_ = max(arr)
    _min_ = min(arr)
    resolution = len(arr)
    offset = 0
    if _min_ < 1:
        while _min_ < 1:
            offset += 1
            _max_ += 1
            _min_ += 1
    for index in range(resolution):
        price = arr[index] + offset
        weight = round((price/_max_) * 10)
        ret_data.append(weight)

    return ret_data

def diff_factor_range(arr: list) -> list:
    '''
        higher diff factors means higher fluctuation
        ranges from: 1
        min price = 1
        if max price = 4 -> max price is 4 times higher than min price

        handling negative numbers:
            we create an offset from the minimum value so that it becomes
            positive thus creating a fix for the calculation
    '''
    ret_data = []
    _max_ = max(arr)
    _min_ = min(arr)
    resolution = len(arr)
    offset = 0
    if _min_ <= 0:
        offset = 1 + abs(_min_)
        _min_ += offset

    for index in range(resolution):
        price = arr[index] + offset
        diff_factor = round(price/_min_, 2)
        ret_data.append(diff_factor)
    return ret_data

def fixed_priority_level(arr: list):
    '''
        the fixed priority values are non-inflated which means that there is
        a fixed amount of values that are spread out for each price index

        ..with other words, it guarantees that devices needing to draw at least X amount of k/Wh every day
        will do exactly that assuming the device (or smart-controller) implements these values correctly
    '''
    pass

def dynamic_priority_level(arr: dict) -> dict:
    '''
        the dynamic priority values are inflated/deflated which means that there is
        a variable amount of values that are spread out for each price index

        this is so that devices that demands a minimum but fixed amount of power-draw
        can reliably run even during days where prices fluctuates
    '''
    pass
