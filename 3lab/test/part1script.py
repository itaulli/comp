"""
Created: Tue Feb 13 13:04:20 2018
Author: Ian Taulli
Description:
"""
import numpy as np
import matplotlib.pyplot as plt
import derivatives as d

#define the functions
def exp(x):
    return np.exp(x)
def log(x):
    return np.log(x+1)
def sin(x):
    return np.sin(2*x)


#define the data dictionary
fun_points = np.linspace(0,2*np.pi,100)
init = np.zeros(len(fun_points))
level2 = {'1true':init,'1forward':init, '1symmetric':init, '2true':init, '2approx':init}
data = {'exp': level2, 'log': level2, 'sin': level2}

#set up the data arrays and save them for a given step size
data['exp']['1true'] = np.exp(fun_points)
data['exp']['2true'] = np.exp(fun_points)
data['log']['1true'] = 1/(fun_points+1)
data['log']['2true'] = -1/(fun_points+1)**2
data['sin']['1true'] = 2*np.cos(2*fun_points)
data['sin']['2true'] = -4*np.sin(2*fun_points)

def data_fill(step_size):
    call = {'exp':exp, 'log':log, 'sin':sin}
    for key in data:
        data[key]['1forward'] = d.FirstForward(call[key],fun_points,step_size)
        data[key]['1symmetric'] = d.FirstSymmetric(call[key],fun_points,step_size)
        data[key]['2approx'] = d.Second3Point(call[key],fun_points,step_size)
    return 'done'

#start evaluating median errors for given step sizes
number_evals = 100
init2 = np.zeros(number_evals)
level3 = {'1true':init2,'1forward':init2, '1symmetric':init2, '2true':init2, '2approx':init2}
error = {'exp': level2, 'log': level2, 'sin': level2}
names1('exp','log','sin')
for i, size in enumerate(np.linspace(1e-14,0.1,number_evals)):
    data_fill(size)    
    for key1, key2 in data.items():
        if key2 == '2approx':
            error[key1][key2][i] = np.median(d.RelativeError(data[key1][key2],data[key1]['2true']))
        else:
            error[key1][key2][i] = np.median(d.RelativeError(data[key1][key2],data[key1]['1true']))