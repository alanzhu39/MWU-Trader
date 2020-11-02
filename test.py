import json
import numpy as np
from updates import *

data = np.loadtxt('data.csv', delimiter=',')
efile = open('extra.json', 'r')
extra = json.load(efile)
efile.close()

n = extra['n']
T = extra['T']
bounds = extra['bounds']

best = T
for i in range(n):
    running = 0
    for t in range(1, T):
        running += (data[t][i]/data[t-1][i]-bounds[1])/(bounds[0]-bounds[1])
    best = min(best, running)

print(best)
