"""
Created on Thu Feb 15 14:28:42 2018
Author: Ian Taulli
Discription: trapezoidal and Simpson integration routines
"""
import numpy as np

def trap(function, N, xmin, xmax):
    interval = (xmax - xmin)/N
    xvals = np.arange(xmin, xmax+interval, interval)
    yvals = function(xvals)
    integral = 0.5*interval*(yvals[0]+yvals[-1])+interval*np.sum(yvals[1:-1])
    return integral

def simpson(function, N, xmin, xmax):
    interval = (xmax - xmin)/N
    half = 0.5*interval
    xvals = np.arange(xmin, xmax+half, half)
    yvals = function(xvals)
    integral = half/3.0*(yvals[0]+yvals[-1]) + 4*half/3*(np.sum(yvals[1:-1:2])) + 2*half/3*(np.sum(yvals[2:-2:2]))
    return integral