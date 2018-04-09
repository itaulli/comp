"""
Created: Wed Feb  7 13:46:38 2018
Author: Ian Taulli
Description: impliments different functions for finding errors
"""
import numpy as np
import cpode

class Error(cpode.OdeSolver):

    def __init__(self, power, spring_constant, x0, v0, xvals, vvals, tvals):
        self.p = power
        self.k = spring_constant
        self.x0 = x0
        self.v0 = v0
        self.x = np.array(xvals)
        self.v = np.array(vvals)
        self.t = np.array(tvals)
        self.mass = 1.0
        self.E0 = self.mass*self.v0**2/2+self.k*abs(self.x0)**self.p/self.p
        self.last = int(len(self.x)//10)

    def EnergyError(self):
        x_lastcycle = self.x[-self.last:]
        v_lastcycle = self.v[-self.last:]
        pointwise_error = abs(self.mass*v_lastcycle**2/2.0+self.k*abs(x_lastcycle)**self.p/self.p-self.E0)/self.E0
        avg_error = np.sum(pointwise_error)/len(pointwise_error)
        return avg_error
    
    def CoordError(self):
        x_lastcycle = self.x[-self.last:]
        v_lastcycle = self.v[-self.last:]
        t_lastcycle = self.t[-self.last:]
        amplitude = np.sqrt(2.0*self.E0/self.k)
        angular_freq = np.sqrt(self.k/self.mass)
        true_x = amplitude*np.sin(angular_freq*t_lastcycle)
        dev = abs(x_lastcycle-true_x)
        avg_dev = np.sum(dev)/len(dev)
        return avg_dev
        