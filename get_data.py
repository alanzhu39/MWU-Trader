import json
import pandas as pd
import numpy as np
from yahoo_fin.stock_info import *

num_stocks = 15
num_days = 5242
stock_file = 'DJIA_20y.txt'

fin = open(stock_file, 'r')
stocks = fin.read().split()[:num_stocks]
fin.close()

data = None

for s in stocks:
    print(s)
    ticker = get_data(s, start_date='01/01/2000', end_date='11/1/2020', interval='1d')
    open_array = np.transpose(np.array([ticker['open'].to_numpy()]))
    if open_array.shape[0] != num_days:
        print(open_array.shape[0])
        continue
    if data is None:
        data = open_array
    else:
        data = np.append(data, open_array,axis=1)

np.savetxt('data.csv', data, delimiter=',')

extra = {}
extra['n'] = data.shape[1]
extra['T'] = data.shape[0]
bounds = [0,0]
for s in range(extra['n']):
    for i in range(1, extra['T']):
        ratio = np.log(data[i][s]/data[i-1][s])
        bounds[0] = min(ratio, bounds[0])
        bounds[1] = max(ratio, bounds[1])
extra['bounds'] = (bounds[0], bounds[1])
extra['r'] = np.exp(bounds[0] - bounds[1])

with open("extra.json", "w") as outfile:
    json.dump(extra, outfile)
