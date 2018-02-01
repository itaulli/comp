"""
Created: Tue Jan 30 11:18:02 2018
Author: Ian Taulli
Description: solves the quadriatic equation in two different ways (excersise in subtractive cancellation)
"""
import numpy as np

def standard(a,b,c):
    x1 = 1/(2*a)*(-b-np.sqrt(b**2-4*a*c))
    x2 = 1/(2*a)*(-b+np.sqrt(b**2-4*a*c))
    return x1, x2

def modified(a,b,c):
    x1 = -1/(2*a)*(b+np.sign(b)*np.sqrt(b**2-4*a*c))
    x2 = c/(a*x1)
    return x1, x2