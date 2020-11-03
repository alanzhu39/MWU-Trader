import json
import pandas as pd
import numpy as np
from yahoo_fin.stock_info import *

num_stocks = 30

fin = open('stock_list.txt', 'r')
stocks = fin.read().split()[:num_stocks]
fin.close()

data = None

for s in stocks:
    ticker = get_data(s, start_date='01/01/2000', end_date='11/01/2020', interval='1d')
    open_array = np.transpose(np.array([ticker['open'].to_numpy()]))
    print(s)
    print(open_array.shape)
    if data is None:
        data = open_array
    else:
        data = np.append(data, open_array,axis=1)

np.savetxt('data.csv', data, delimiter=',')

extra = {}
extra['n'] = data.shape[1]
extra['T'] = data.shape[0]
bounds = [0,0]
r = 2
for s in range(extra['n']):
    for i in range(1, extra['T']):
        r = min(r, data[i][s]/data[i-1][s])
        ratio = np.log(data[i][s]/data[i-1][s])
        bounds[0] = min(ratio, bounds[0])
        bounds[1] = max(ratio, bounds[1])
extra['bounds'] = (bounds[0], bounds[1])
extra['r'] = r

with open("extra.json", "w") as outfile:
    json.dump(extra, outfile)
