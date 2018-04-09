"""
Created: Sun Mar  4 20:39:25 2018
Author: Ian Taulli
Description:
"""
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
pool = Pool(4)

class TestClass:
    
    def __init__(self, power):
        self.p = power
    def fun(self, x):
        return x**self.p

instance = TestClass(2)
vals = np.arange(1,10)
y = pool.map(instance.fun, vals)
print(y)