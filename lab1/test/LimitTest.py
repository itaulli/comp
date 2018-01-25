"""
Created on Thu Jan 25 14:31:46 2018
Author: Ian Taulli
Discription:
"""
import numpy as np
import matplotlib.pyplot as plt


for i in range(400):
    
    n = 10.0**i

    if type(n) != float:
        break
    else:
        print(i)