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
r = extra['r']
start = 100000

def test_simple():
    for k in range(1, 20):
        epsilon = k/20
        portfolio = np.full(n, start/n)
        weights = np.full(n, 1/n)
        running_value = np.array([start])
        running_loss = 0

        for t in range(1, T):
            losses = np.copy(data[t])
            for i in range(len(losses)):
                portfolio[i] *= data[t][i]/data[t-1][i]
                val = min(bounds[1], max(bounds[0], np.log(data[t][i]/data[t-1][i])))
                losses[i] = (val - bounds[1])/(bounds[0]-bounds[1])
            running_value = np.append(running_value, np.sum(portfolio))
            running_loss += np.dot(weights, losses)
            update_simple(weights, losses, epsilon)
            rebalance(portfolio, weights)

        print("epsilon: ",epsilon,"\treturn: ",running_value[-1]/start,'\tcum loss:',running_loss)

def test_EG():
    for k in range(1, 20):
        eta = k/200
        portfolio = np.full(n, start/n)
        weights = np.full(n, 1/n)
        running_value = np.array([start])
        running_loss = 0

        for t in range(1, T):
            losses = np.copy(data[t])
            for i in range(len(losses)):
                portfolio[i] *= data[t][i]/data[t-1][i]
                losses[i] = data[t][i]/data[t-1][i]
            running_value = np.append(running_value, np.sum(portfolio))
            running_loss += np.log(np.dot(weights, losses))
            update_EG(weights, losses, eta)
            rebalance(portfolio, weights)

        print("eta: ",eta,"\treturn: ",running_value[-1]/start,'\tcum gain:',running_loss)

if __name__ == "__main__":
    test_EG()
