import pandas as pd
import numpy as np
from yahoo_fin.stock_info import *

fin = open('stock_list.txt', 'r')
stocks = fin.read().split()

data = None

for s in stocks:
    ticker = get_data(s, start_date='01/01/2010', end_date='11/01/2020', interval='1d')
    open_array = np.transpose(np.array([ticker['open'].to_numpy()]))
    if data is None:
        data = open_array
    else:
        data = np.append(data, open_array,axis=1)

np.savetxt('data.csv', data, delimiter=',')
