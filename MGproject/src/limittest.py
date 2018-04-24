"""
Created: Mon Apr 16 23:09:27 2018
Author: Ian Taulli
Description:
"""
import numpy as np
import matplotlib.pyplot as plt

n = 1e8

limit = int(np.log2(n))

yvals = [n,]
xvals = [0,]
for i in range(1,limit+1):
    n = n//2+1
    yvals.append(n)
    xvals.append(i)

for i in range(len(xvals)):
    print(xvals[i], '-->', yvals[i])