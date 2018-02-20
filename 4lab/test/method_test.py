"""
Created on Thu Feb 15 14:35:06 2018
Author: Ian Taulli
Discription:
"""
import numpy as np
import matplotlib.pyplot as plt
from custom_integrals import *
import math
import gaussLegendreQuadrature as glq

#define the relavant functions
def exp(x):
    return np.exp(x)

def log(x):
    return np.log(x+1)

def sin(x):
    return (np.sin(2*x))**2

#define the integration limits
x_min = 0.0
x_max = 2*np.pi

#define the exact integrals
exact = np.zeros(3)
exact[0] = np.exp(x_max) - np.exp(x_min)
exact[1] = ((x_max+1)*np.log(x_max+1)-x_max) - ((x_min+1)*np.log(x_min+1)-x_min)
exact[2] = (0.5*x_max-0.25*np.sin(2*x_max)*np.cos(2*x_max)) - (0.5*x_min-0.25*np.sin(2*x_min)*np.cos(2*x_min))

#name the methods and functions
methods = (glq.integrate, trap, simpson)
functions = (exp, log, sin)


for N in np.arange(1,101):
    for i, function in enumerate(functions):
        for method in methods:
            approx = method(function, N, x_min, x_max)
            rel_error[i] = abs(approx-exact[i])/exact[i]