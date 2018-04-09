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
exact[2] = ((0.5*x_max-0.25*np.sin(2*x_max)*np.cos(2*x_max)) - 
            (0.5*x_min-0.25*np.sin(2*x_min)*np.cos(2*x_min)))

#name the methods and functions
methods = (glq.integrate, trap, simpson)
functions = (exp, log, sin)
call_m = {glq.integrate: 'Quadrature', trap: 'Trapezoidal', simpson: 'Simpson'}
call_f = {exp: 'exp', log: 'log', sin: 'sin'}

#set up the arrays to iterate over
powers = np.arange(1,10)
N = np.power(2, powers)

for i, function in enumerate(functions):
    plt.figure()
    for method in methods:
        error_vals = np.array(0)
        for n in N:
            approx = method(function, n, x_min, x_max)
            rel_error = np.array(abs((approx-exact[i])/exact[i]))
            #if the deviation is within the machine precision do this
            #to avoid taking the logarithm of 0 (epsilon = 1e-16)
            if rel_error == 0.0:
                rel_error = 1e-16/exact[i]
            error_vals = np.hstack((error_vals, rel_error))
        error_vals = error_vals[1:]
        #plot_N = np.log10(N+1)
        #plot_error = np.log10(error_vals+1)
        plt.loglog(N, error_vals, label=call_m[method])
    ax = plt.gca()
    ax.grid(True)
    ax.set_title('Relative error for '+call_f[function])
    ax.set_xlabel('number of intervals')
    ax.set_ylabel('relative error')
    ax.legend()
    plt.savefig('error_plot_'+call_f[function]+'.pdf')
    plt.close()