"""
Created on Thu Feb 15 14:35:06 2018
Author: Ian Taulli
Discription:
"""
import numpy as np
import matplotlib.pyplot as plt
import custom_derivatives as cd

def fun(x):
    return x**2

print(cd.simpson(fun, 100, 0, 10))