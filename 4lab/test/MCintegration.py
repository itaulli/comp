"""
Created: Wed Feb 21 14:48:09 2018
Author: Ian Taulli
Description:
"""
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import uniform
import os
import struct
from numpy.random import seed
import sobol
myseed = abs(struct.unpack('i', os.urandom(4))[0])
seed(myseed)

#function which retruns Nmax number of random 10-dimensional points
def pseudo_rand(Nmax):
    points = np.zeros(10)
    N = 0
    for i in range(Nmax):
        point = np.array(uniform(0.0, 1.0, 10))
        points = np.vstack((points,point))
    points = points[1:]    
    return points

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

#tuple of N values to iterate over
num_evals = (1e2, 3e2, 1e3, 3e3, 1e4, 3e4, 1e5)
bin_nums = [10, 20, 30, 50, 80, 100, 100]

#initialize a couple of arrays to store the plot points
bias_plot = np.array([])
std_plot = np.array([])
for k, n in enumerate(num_evals):
    
    #the arrays that will be summed over for the averages
    bias_array = np.array([])
    std_array = np.array([])
    pull_array = np.array([])
    
    #do the approximation a bunch of times and average out the results
    if n == (1e2, 3e2, 1e3, 3e3, 1e4):
        repeat = 100
    else:
        repeat = 5
    for i in range(repeat):
        unpack = mc_int(pseudo_rand(n))
        bias_array = np.hstack((bias_array,unpack[1]))
        std_array = np.hstack((std_array,unpack[2]))
        pull_array = np.hstack((pull_array,unpack[3]))
    
    avg_bias = np.sum(bias_array)/len(bias_array)
    avg_std = np.sum(std_array)/len(std_array) 
    bias_plot = np.hstack((bias_plot,avg_bias))
    std_plot = np.hstack((std_plot,avg_std))
    
    #plot the pull histogram for this n before moving on to the next one
    plt.figure()
    plt.hist(pull_array,bins=bin_nums[k],normed=1)
    ax = plt.gca()
    ax.grid(True)
    ax.set_title('Pull distribution N = {:d}'.format(int(n)))
    ax.set_xlabel('pull value')
    ax.set_ylabel('frequency')
    plt.savefig('pull_hiso_{:d}.pdf'.format(int(n)))
    plt.close()
    print('done with N = {:d}'.format(int(n)))
    