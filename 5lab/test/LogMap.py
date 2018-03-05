"""
Created: Thu Jul 13 22:27:58 2017
Author: Ian Taulli
Description: Log Map (bifrucation)
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from multiprocessing import Pool
#from imageArray2d import imageArray2d

def function(ratio):
    temp1 = [0,0]
    temp2 = [0,0]
    for y in np.linspace(0.1,.9,8):
        for i in range(1000):
            y=ratio*y*(1-y) #the fractal mapping itself
            if i > 800: #allow some iterations for the fractal to come to its fixed point
                point = round(y,3)
                temp1 = [ratio,point] #saves the data from this iteration as a set of points
                temp2 =  np.vstack((temp2,temp1)) #adds the point from this iteration to the array of all of the points
    temp2 = temp2[1:,:]
    return temp2

ratios = np.linspace(3.56,3.6,1000)
p = Pool(10)
data = p.map(function, ratios)

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
plt.title('Logistic Map')
plt.xlabel('ratio')
plt.ylabel('population')
plt.savefig('test.pdf', format='pdf')
plt.close()

'''
plt.figure(figsize=(20,20))
xmin = 0.9
xmax = 4.1
number_of_x_cells = 1000
number_of_y_cells = 800
ymin = 0
ymax = 1
cells = imageArray2d(x_plot, y_plot, number_of_x_cells, xmin, xmax, number_of_y_cells, ymin, ymax)
range_ratio = (xmax - xmin)*1.0/(ymax - ymin)
plt.imshow(cells, cmap=plt.cm.binary, origin='lower',
       interpolation='nearest', extent=(xmin, xmax, ymin, ymax),
       aspect=number_of_y_cells*range_ratio/number_of_x_cells)
ax = plt.gca()
ax.set_title('Logistic Map')
ax.set_xlabel('ratio')
ax.set_ylabel('population')
plt.savefig('test.pdf')
plt.close()
'''