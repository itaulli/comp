"""
Created: Thu Mar  1 13:39:43 2018
Author: Ian Taulli
Description:
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import pandas as pd
from multiprocessing import Pool
from PendulumAngles import *

startTime = time.time()

F_D = np.arange(0.5,2.5,0.0015)
#F_D = (0.5, 1.2)
theta_0 = np.linspace(0, 1, 200)

def function(f):
    x_array = np.array([])
    for theta in theta_0:
        x = PendulumAngles(theta, f)
        x_array = np.hstack((x_array,x))     
    return x_array

p = Pool(4)
data = p.map(function, F_D)
x_raw = np.ravel(data)

f_array = np.zeros(len(x_raw))
for i in range(len(F_D)):
    n_each = int(len(x_raw)/len(F_D))
    f_array[i*n_each:(i+1)*n_each] = F_D[i]
    

df = pd.DataFrame({'x':f_array, 'y':x_raw})
no_doops = df.drop_duplicates()
x_plot = np.asarray(no_doops['x'])
y_plot = np.asarray(no_doops['y'])

plt.figure(figsize=(80,80))

SMALL_SIZE = 50
MEDIUM_SIZE = 80
BIGGER_SIZE = 120
plt.rc('axes', titlesize=BIGGER_SIZE)
plt.rc('axes', labelsize=MEDIUM_SIZE)    
plt.rc('xtick', labelsize=SMALL_SIZE)    
plt.rc('ytick', labelsize=SMALL_SIZE)    
plt.rc('figure', titlesize=BIGGER_SIZE)

plt.plot(x_plot,y_plot,'b,') #places a pixel ',' to mark each point
plt.title('Pendulum Bifrucation')
plt.xlabel('magnitude F_D')
plt.ylabel('angles')
plt.savefig('test.pdf', format='pdf')
plt.close()
