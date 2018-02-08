"""
Created on Thu Feb  8 14:15:47 2018
Author: Ian Taulli
Discription:
"""
import numpy as np

def FirstForward(function, eval_point, step_size):
    f = function
    x = eval_point
    h = step_size
    return (f(x+h)-f(x))/h

def FirstSymmetric(function, eval_point, step_size):
    f = function
    x1 = eval_point + step_size
    x2 = eval_point - step_size
    two_h = x1 - x2
    return (f(x1)-f(x2))/two_h    