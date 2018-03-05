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

startTime = datetime.now()

Mag_F = (0.5, 1.2, 1.35, 1.44, 1.5)
theta_0 = np.linspace(0, 1, 200)
omegaD = 2.0/3.0
periodD = 2*np.pi/omegaD
period_times = np.arange(200*periodD,400*periodD,periodD)

x_stack = np.array([])
f_stack = np.array([])
for f in Mag_F:
    print('doing F = {:.3f}'.format(f))
    x_array = np.array([])
    for theta in theta_0:
        x = PendulumAngles(theta, f)
        x_array = np.hstack((x_stack,x))
    f_array = f*np.ones(len(x_array))
    x_stack = np.hstack((x_stack,x_array))
    f_stack = np.hstack((f_stack,f_array))

df = pd.DataFrame({'x':f_stack, 'y':x_stack})
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