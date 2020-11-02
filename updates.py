import numpy as np

def update_simple(weights, losses, epsilon):
    # Updates weight series with losses and simple formula
    # Normalized, in place
    total = 0
    for i in range(len(weights)):
        weights[i] *= (1 - epsilon)**losses[i]
        total += weights[i]
    for i in range(len(weights)):
        weights[i] = weights[i]/total

def update_EG(weights, losses, eta):
    # Updates weight series with expoentiated gradient update
    # Normalized, in place
    pass

def rebalance(portfolio, weights):
    # Rebalances portfolio series with new weight series
    # In place
    total = np.sum(portfolio)
    for i in range(len(portfolio)):
        portfolio[i] = weights[i]*total
