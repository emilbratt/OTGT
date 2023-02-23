from statistics import mean
import numpy as np 
def slope(arr: list) -> int:
    '''
        used to move priority towards the lower end

        range from 1 (flat)
        1.5 = max price is  50% more than mean e.g. 150 to 100
        2.0 = max price is 100% more than mean e.g. 200 to 100
        2.5 = max price is 250% more than mean e.g. 250 to 100
        ..spikes and dips only affect the slope by a small margin
    '''
    # push all numbers to a positive value if needed
    _min_ = min(arr)
    if _min_ < 0:
        new_list = []
        offset = 0
        while _min_ < 1:
            offset += 1
            _min_ += 1
        for val in arr:
            new_list.append(val+offset)
        arr = new_list
    _mean_ = mean(arr)
    _max_ = max(arr)
    _min_ = min(arr)
    try:
        slope = round((_max_ / _mean_), 1)
    except ZeroDivisionError:
        slope = 1.0
    return float(slope)

def spike(arr: list) -> int:
    '''
        used to
            ..reduce priority on the higher values if positive
            ..increase priority on the lower values if negative

        range from - (dip) to + (spike)
             -N
            -50 = massive dip
            -10 = small dip
              0 = no spike
            +10 = small spike
            +50 = massive spike
             +N

        difference between mean, min and max value is calculated
    '''
    # push all numbers to a positive value if needed
    _min_ = min(arr)
    if _min_ < 0:
        new_list = []
        offset = 0
        while _min_ < 1:
            offset += 1
            _min_ += 1
        for val in arr:
            new_list.append(val+offset)
        arr = new_list
    _mean_ = round(mean(arr))
    _max_ = max(arr)
    _min_ = min(arr)
    spike = (_max_ - _mean_) - (_mean_ - _min_)
    try:
        slope = _max_ / _mean_
    except ZeroDivisionError:
        slope = 1.0
    spike = round(spike/slope)
    return spike
