import json
import numpy as np
from updates import *
import matplotlib.pyplot as plt
import sys

data = np.loadtxt('data.csv', delimiter=',')
efile = open('extra.json', 'r')
extra = json.load(efile)
efile.close()

n = extra['n']
T = extra['T']
bounds = extra['bounds']
r = extra['r']
start = 100000

def test_splits(split_size, eta,do_plot):
    fig, axs = plt.subplots(2*n // split_size)
    for k in range(n // split_size):
        curr_data = data[:,k*split_size:(k+1)*split_size]
        portfolio = np.full(split_size, start/split_size)
        weights = np.full(split_size, 1/split_size)
        running_value = np.array([start])
        running_loss = 0
        running_weights = np.array([np.copy(weights)]).T

        for t in range(1, T):
            losses = np.copy(curr_data[t])
            for i in range(len(losses)):
                portfolio[i] *= curr_data[t][i]/curr_data[t-1][i]
                losses[i] = curr_data[t][i]/curr_data[t-1][i]
            running_value = np.append(running_value, np.sum(portfolio))
            running_loss += np.log(np.dot(weights, losses))
            update_EG(weights, losses, eta)
            running_weights = np.append(running_weights, np.array([np.copy(weights)]).T, axis=1)
            rebalance(portfolio, weights)

        print("eta: ",eta,"\treturn: ",running_value[-1]/start,'\tcum gain:',running_loss)

        axs[k*2].plot(running_value)
        for i in range(len(running_weights)):
            axs[k*2 + 1].plot(running_weights[i])
        plot_best_split(axs[k*2], curr_data)
    if do_plot:
        plt.show()

def plot_best_split(plot_in, prices):
    best = np.array([start])
    ind = 0
    for i in range(prices.shape[1]):
        running = np.array([start])
        for t in range(1, T):
            running = np.append(running, running[-1]*prices[t][i]/prices[t-1][i])
        if running[-1] > best[-1]:
            best = running
            ind = i
    print('best value: ',best[-1]/start)
    plot_in.plot(best)

if __name__ == "__main__":
    size_in = int(sys.argv[1])
    eta_in = float(sys.argv[2])
    if len(sys.argv) > 3:
        plot_in = sys.argv[3] == 'True'
    else:
        plot_in = False
    test_splits(size_in, eta_in, plot_in)
