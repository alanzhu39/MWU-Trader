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
start = 100000
running = 0
epsilon = 0.25

for k in range(1, 45):
    epsilon = k/100
    running = 0
    portfolio = np.full(n, start/n)
    weights = np.full(n, 1/n)

    for t in range(1, T):
        losses = np.copy(data[t])
        for i in range(len(losses)):
            portfolio[i] *= data[t][i]/data[t-1][i]
            losses[i] = (data[t][i]/data[t-1][i]-bounds[1])/(bounds[0]-bounds[1])
        running += np.dot(losses, weights)
        update_simple(weights, losses, epsilon)
        rebalance(portfolio, weights)

    print("epsilon: ",epsilon)
    print("result: ",running)
