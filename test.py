import json
import numpy as np
from updates import *

data = np.loadtxt('data.csv', delimiter=',')
efile = open('extra.json', 'r')
extra = json.load(efile)
efile.close()

stock_file = 'DJIA_20y.txt'

fin = open(stock_file, 'r')
stocks = fin.read().split()
fin.close()

n = extra['n']
T = extra['T']
bounds = extra['bounds']

def test_loss_simple():
    best = T
    ind = 0
    for i in range(n):
        running = 0
        for t in range(1, T):
            val = min(bounds[1], max(bounds[0], np.log(data[t][i]/data[t-1][i])))
            running += (val-bounds[1])/(bounds[0]-bounds[1])
        if running < best:
            best = running
            ind = i
    print('loss:',best,'\tstock:',stocks[ind])

def test_gain_EG():
    best = 0
    ind = 0
    for i in range(n):
        running = 0
        for t in range(1, T):
            running += np.log(data[t][i]/data[t-1][i])
        if running > best:
            best = running
            ind = i
    print('gain:',best,'\tstock:',stocks[ind])

def test_return():
    best = 1
    ind = 0
    for i in range(n):
        running = 1
        for t in range(1, T):
            running *= data[t][i]/data[t-1][i]
        if running > best:
            best = running
            ind = i
    print('return:',best,'\tstock:',stocks[ind])

if __name__ == "__main__":
    test_gain_EG()
    test_return()
