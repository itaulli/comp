"""
Created: Mon Feb 26 16:09:49 2018
Author: Ian Taulli
Description:
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import struct
from numpy.random import seed
import sobol
myseed = abs(struct.unpack('i', os.urandom(4))[0])
seed(myseed)

#function which returns Nmax number of Sobol-random 10-dimensional points
def sobol_rand(Nmax):
    sobol.init(10)
    points = np.zeros(10)
    for i in range(Nmax):
        point = np.array(sobol.next())
        points = np.vstack((points,point))
    points = points[1:]
    return points

#funciton which does the approxamation and calculates the relavent parameters
def mc_int(points):
    truth = 155.0/6.0
    fun_array = np.array([])
    
    for i in range(len(points)):
        one_point = points[i]
        fun_eval = np.sum(one_point)**2
        fun_array = np.hstack((fun_array,fun_eval))
    
    avg_fun = np.sum(fun_array)/len(fun_array)
    avg_fun2 = np.sum(fun_array**2)/len(fun_array)
    
    bias = np.sum(fun_array-truth)/len(fun_array)
    std = np.sqrt(np.sum((fun_array-avg_fun)**2)/len(fun_array))
    
    est_uncert = np.sqrt((avg_fun2-avg_fun**2)/len(fun_array))
    pull = (fun_array-truth)/est_uncert
    
    return avg_fun, bias, std, pull


squence = sobol_rand(2**17)

powers = (6,7,8,9,10,11,12,13,14,15,16,17)
num_evals = np.power(2, powers)
truth = 155.0/6.0
abs_error = []

for n in num_evals:
    points = sequence[:n+1]
    approx, bias, std, pull = mc_int(points)
    n_error = abs(approx - truth)
    abs_error.append(n_error)

plt.loglog(num_evals, abs_error)
ax = plt.gca()
ax.set_title('Convergence for Quasi-MC Integration')
ax.set_xlabel('number of points')
ax.set_ylabel('absolute error')
plt.savefig('Sobol_error.pdf')
plt.close()
    
    