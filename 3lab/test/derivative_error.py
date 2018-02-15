"""
Created: Wed Feb 14 10:05:08 2018
Author: Ian Taulli
Description: calculates the median error for different derivative algoithms as
             as a function of step size
"""
import numpy as np
import matplotlib.pyplot as plt
from derivatives import *

#define the functions
def exp(x):
    return np.exp(x)
def log(x):
    return np.log(x+1)
def sin(x):
    return np.sin(2*x)


#define the approximation space
x_array = np.linspace(0,2*np.pi,100)

#calculate the true derivatives
exp_true = np.exp(x_array)
log_1true = 1/(x_array+1)
log_2true = -1/(x_array+1)**2
sin_1true = 2*np.cos(2*x_array)
sin_2true = -4*np.sin(2*x_array)

#makes lists and dictionaries that allow automation of naming
functions = (exp, log, sin)
methods = (FirstForward, FirstSymmetric, Second3Point)
call_true = {'exp_1true': exp_true, 'exp_2true': exp_true, 'log_1true': log_1true,\
             'log_2true': log_2true, 'sin_1true': sin_1true, 'sin_2true': sin_2true}
call_f = {exp: 'exp', log: 'log', sin: 'sin'}
call_m = {FirstForward: 'first forward', FirstSymmetric: 'first symmetric', Second3Point: 'second 3-point'}

#run the loop for the approximations and save the median errors to a graph
step_sizes = np.linspace(1e-14, 0.1, 2000)

for function in functions:
    plt.figure()
    for method in methods:
        medians = np.zeros(len(step_sizes))
        for i, size in enumerate(step_sizes):
            approx = method(function, x_array, size)
            if method == Second3Point:
                error = RelativeError(approx, call_true[call_f[function]+'_2true'])
            else:
                error = RelativeError(approx, call_true[call_f[function]+'_1true'])
            medians[i] = np.median(error)
        plt.loglog(step_sizes, medians, linewidth=1.0, label=call_m[method])
    
    #decorate the plots    
    ax = plt.gca()
    ax.grid(True)
    ax.set_title('errors for '+call_f[function])
    ax.set_xlabel('step size')
    ax.set_ylabel('relative error')
    lines = ax.get_lines()
    ax.legend(fontsize=10)
    plt.savefig('derivatives_'+call_f[function]+'.pdf')
    plt.close()         