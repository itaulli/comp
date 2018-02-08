"""
Created: Thu Feb  1 22:40:42 2018
Author: Ian Taulli
Description:
"""
import numpy as np
import cpforces

class Pforce(cpforces.BasicForce):
    """
    calculates the force F = -|x|^p/x
    corresponding to U = |x|^p/p
    """
    def __init__(self, power, spring_constant):
        self.p = power
        self.k = spring_constant
    def __call__(self, t, x, v):
        return -1.0*self.k*np.sign(x)*abs(x)**(self.p-1.0)
        
    
