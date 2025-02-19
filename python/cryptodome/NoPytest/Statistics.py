import numpy as np

def calc_mean_std(data):
    mean = np.mean(data)
    std = np.std(data)
    return mean, std