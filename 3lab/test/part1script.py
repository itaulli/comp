"""
Created: Tue Feb 13 13:04:20 2018
Author: Ian Taulli
Description:
"""
import numpy as np
import matplotlib.pyplot as plt
import derivatives as d

#define the functions
def exponent(x):
    return np.exp(x)
def log(x):
    return np.log(x+1)
def sin(x):
    return np.sin(2*x)


#define the data dictionary
fun_points = np.linspace(0,2*np.pi,100)
level2 = {'1true','1forward', '1symmetric', '2true', '2approx'}
data = {'exp': level2, 'log': level2, 'sin': level2}

#set up the data arrays and save them for a given step size
data['exp']['1true'] = np.exp(fun_points)
data['exp']['2true'] = np.exp(fun_points)
data['log']['1true'] = 1/(fun_points+1)
data['log']['2true'] = -1/(fun_points+1)**2
data['sin']['1true'] = 2*np.cos(2*fun_points)
data['sin']['2true'] = -4*np.sin(2*fun_points)

def data_fill(step_size):
    data['exp']['1forward'] = d.FirstForward(exponent,fun_points,step_size)
    data['exp']['1symmetric'] = d.FirstSymmetric(exponent,fun_points,step_size)
    data['exp']['2approx'] = d.Second3Point(exponent,fun_points,step_size)
    data['log']['1forward'] = d.FirstForward(log,fun_points,step_size)
    data['log']['1symmetric'] = d.FirstSymmetric(log,fun_points,step_size)
    data['log']['2approx'] = d.Second3Point(log,fun_points,step_size)
    data['sin']['1forward'] = d.FirstForward(sin,fun_points,step_size)
    data['sin']['1symmetric'] = d.FirstSymmetric(sin,fun_points,step_size)
    data['sin']['2approx'] = d.Second3Point(sin,fun_points,step_size)
    return 'done'