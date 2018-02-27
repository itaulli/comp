"""
Created: Wed Feb 21 14:48:09 2018
Author: Ian Taulli
Description:
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy.random import uniform
import os
import struct
from numpy.random import seed
myseed = abs(struct.unpack('i', os.urandom(4))[0])
seed(myseed)

#function which retruns Nmax number of random 10-dimensional points
def pseudo_rand(Nmax):
    points = np.zeros(10)
    for i in range(int(Nmax)):
        point = np.array(uniform(0.0, 1.0, 10))
        points = np.vstack((points,point))
        if i % 10000 == 0 and i != 0:
            print('stacking number = {:d}'.format(i))
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
    
    bias = avg_fun-truth
    std = np.sqrt(np.sum((fun_array-avg_fun)**2)/len(fun_array))
    
    est_uncert = np.sqrt((avg_fun2-avg_fun**2)/len(fun_array))
    pull = (avg_fun-truth)/est_uncert
    
    return avg_fun, bias, std, pull

#tuple of N values to iterate over
num_evals = (1e2, 3e2, 1e3, 3e3, 1e4, 3e4, 1e5)

#initialize a couple of arrays to store the plot points
bias_plot = np.array([])
std_plot = np.array([])
for k, n in enumerate(num_evals):
    
    #the arrays that will be summed over for the averages
    bias_array = np.array([])
    std_array = np.array([])
    pull_array = np.array([])
    
    #do the approximation a bunch of times and average out the results
    for i in range(100):
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
    plt.hist(pull_array,bins=10,normed=1)
    ax = plt.gca()
    ax.grid(True)
    ax.set_title('Pull distribution N = {:d}'.format(int(n)))
    ax.set_xlabel('pull value')
    ax.set_ylabel('frequency')
    plt.savefig('pull_hiso_{:d}.pdf'.format(int(n)))
    plt.close()
    print('done with N = {:d}'.format(int(n)))

#plot the bias vs N
plt.figure()
plt.plot(num_evals, bias_plot)
ax = plt.gca()
ax.grid(True)
ax.set_title('Average Bias Over All Trials')
ax.set_xlabel('number of function evaluations per trial')
ax.set_ylabel('bias')
plt.savefig('bias_plot.pdf')
plt.close()

#loglog plot of std vs N
plt.figure()
plt.semilogx(num_evals, std_plot)
ax = plt.gca()
ax.grid(True)
ax.set_title('Average Standard Deviation Over All Trials')
ax.set_xlabel('number of function evaluations per trial')
ax.set_ylabel('standard deviation')
plt.savefig('std_plot.pdf')
plt.close()
    
