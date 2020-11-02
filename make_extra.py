import json
import numpy as np

data = np.loadtxt('data.csv', delimiter=',')

extra = {}
extra['n'] = data.shape[1]
extra['T'] = data.shape[0]
bounds = [1.0,1.0]
for s in range(extra['n']):
    for i in range(1, extra['T']):
        ratio = data[i][s] / data[i-1][s]
        bounds[0] = min(ratio, bounds[0])
        bounds[1] = max(ratio, bounds[1])
extra['bounds'] = (bounds[0], bounds[1])

with open("extra.json", "w") as outfile:
    json.dump(extra, outfile)
