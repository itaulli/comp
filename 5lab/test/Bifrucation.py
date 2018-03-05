"""
Created: Thu Mar  1 13:39:43 2018
Author: Ian Taulli
Description:
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PendulumAngles import *
from datetime import datetime
import pandas as pd
from multiprocessing import Pool

startTime = datetime.now()

F_D = (0.5, 1.2, 1.35, 1.44, 1.5)
theta_0 = np.linspace(0, 1, 200)

def function(f):
    print('doing f = {:.4f}'.format(f))
    x_array = np.array([])
    points = np.array([0,0])
    for theta in theta_0:
        x = PendulumAngles(theta, f)
        x_array = np.hstack((x_array,x))
        for x in x_array:
            point = [f, x]
            points = np.vstack((points, point))
    points = points[1:,:]
    return points

p = Pool(2)
data = p.map(function, F_D)
lumpy = np.array(data)
flat = np.ravel(lumpy)
x_raw = flat[0::2]
y_raw = flat[1::2]

df = pd.DataFrame({'x':x_raw, 'y':y_raw})
no_doops = df.drop_duplicates()
x_plot = np.asarray(no_doops['x'])
y_plot = np.asarray(no_doops['y'])

plt.figure(figsize=(80,80))
#plt.ylim((0.3,0.4))
plt.plot(x_plot,y_plot,'k,') #places a pixel ',' to mark each point
plt.title('Pendulum Bifrucation')
plt.xlabel('magnitude F_D')
plt.ylabel('angles')
plt.savefig('test.pdf', format='pdf')
plt.close()

print(startTime - datetime.now())