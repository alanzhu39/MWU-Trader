import json
import pandas as pd
import numpy as np
from yahoo_fin.stock_info import *

num_stocks = 600
stock_file = 'SP500_20y.txt'

fin = open(stock_file, 'r')
start_day = fin.readline()
end_day = fin.readline()
num_days = int(fin.readline())
stocks = fin.read().split()[:num_stocks]
fin.close()

data = None

for s in stocks:
    try:
        ticker = get_data(s, start_date=start_day, end_date=end_day, interval='1d')
        open_array = np.transpose(np.array([ticker['open'].to_numpy()]))
    except:
        print(s)
    if open_array.shape[0] != num_days:
        print(s)
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
