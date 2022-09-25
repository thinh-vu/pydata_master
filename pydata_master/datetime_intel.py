# Copyright 2022 Thinh Vu @ GitHub
# See LICENSE for details.
from datetime import datetime, date
from datetime import timedelta
import pandas as pd

def date_from_today(days_delta, format, backward = True): # Cocate the output string with 'T00:00:00Z' or 'T23:59:59Z' if you need
    """
    Return a DateTime value using today's DateTime as the base.
    Args:
        days_delta (:obj:`int`, required): How many days to add or subtract from today's
        format (:obj:`str`, required): Datetime format of the output. Ex: "%Y-%m-%d"
        format (:obj:`boolean`, optional): True to get dates in the past, False to get the future ones
    """
    today_val = datetime.now()
    if backward == True:
        target = (today_val - timedelta(days_delta)).strftime(format)
    elif backward == False:
        target = (today_val + timedelta(days_delta)).strftime(format)
    else:
        pass
    return target


def date_start_end(format, periods, freq):
    """
    Return a DateTime value using today's DateTime as the base.
    Args:
        format (:obj:`str`, required): Datetime format of the output. Ex: "%Y-%m-%d"
        periods (:obj:`int`, required): How many periods from today
        freq (:obj:`str`, required): datetime frequency code. Ex: 'MS' for Month Start and 'M' for Month End. See more at: 
    """
    today = datetime.now().strftime(format)
    target = pd.date_range(end=today, periods=periods, freq=freq)[0]\
                .strftime('%Y-%m-%d')
    return target