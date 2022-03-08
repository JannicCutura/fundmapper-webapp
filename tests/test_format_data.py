from utils.get_data import format_data, get_data
import pandas as pd, numpy as np

df = format_data(get_data())

assert len(df) > 0, "No data found"
assert list(df[0].keys()) == ['date', 'type', 'investmenttypedomain', 'mean_yield', 'sum_amount', 'color'], "Incorrect columns"



