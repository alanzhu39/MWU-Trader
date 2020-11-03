import json
import numpy as np
from updates import *
import matplotlib.pyplot as plt

data = np.loadtxt('data.csv', delimiter=',')
efile = open('extra.json', 'r')
extra = json.load(efile)
efile.close()

n = extra['n']
T = extra['T']
bounds = extra['bounds']
r = extra['r']
start = 100000

def test_simple(use_range=True,denom=20):
    for k in range(1, 20):
        epsilon = k/denom
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
        if not use_range:
            plt.plot(running_value)
            plt.show()
            break

def test_EG(use_range=True,denom=20):
    for k in range(1, 20):
        eta = k/denom
        portfolio = np.full(n, start/n)
        weights = np.full(n, 1/n)
        running_value = np.array([start])
        running_loss = 0
        running_weights = np.array([np.copy(weights)]).T

        for t in range(1, T):
            losses = np.copy(data[t])
            for i in range(len(losses)):
                portfolio[i] *= data[t][i]/data[t-1][i]
                losses[i] = data[t][i]/data[t-1][i]
            running_value = np.append(running_value, np.sum(portfolio))
            running_loss += np.log(np.dot(weights, losses))
            update_EG(weights, losses, eta)
            running_weights = np.append(running_weights, np.array([np.copy(weights)]).T, axis=1)
            rebalance(portfolio, weights)

        print("eta: ",eta,"\treturn: ",running_value[-1]/start,'\tcum gain:',running_loss)
        if not use_range:
            # plt.plot(running_value)
            for i in range(len(running_weights)):
                plt.plot(running_weights[i])
            # plot_best()
            plt.show()
            break

def plot_best():
    best = np.array([start])
    ind = 0
    for i in range(n):
        running = np.array([start])
        for t in range(1, T):
            running = np.append(running, running[-1]*data[t][i]/data[t-1][i])
        if running[-1] > best[-1]:
            best = running
            ind = i
    plt.plot(best)

if __name__ == "__main__":
    test_EG(True,1)
