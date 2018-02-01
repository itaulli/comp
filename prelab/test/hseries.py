"""
Created: Wed Jan 31 21:28:38 2018
Author: Ian Taulli
Description: harmonic series sum
"""
import numpy as np
import matplotlib.pyplot as plt

def hsum(x):
    old_sum, new_sum = 0.0, 0.0
    for i in np.arange(1,x+1):
        old_sum = new_sum
        new_sum += 1.0/i
    return new_sum