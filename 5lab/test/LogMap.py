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
    for y in np.linspace(0.1,0.9,10):
        for i in range(1000):
            y=ratio*y*(1-y) #the fractal mapping itself
            if i > 800: #allow some iterations for the fractal to come to its fixed point
                point = round(y,3)
                temp1 = [ratio,point] #saves the data from this iteration as a set of points
                temp2 =  np.vstack((temp2,temp1)) #adds the point from this iteration to the array of all of the points
    temp2 = temp2[1:,:]
    return temp2

def justx(ratio):
    points = np.ravel(function(ratio))
    xvals = points[1::2]
    return xvals

#part3    

ratios = np.linspace(3.4,3.8,1000)
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
#plt.savefig('test.pdf', format='pdf')
#plt.close()

'''
#part2

xvals1 = justx(3.3)
xvals2 = justx(3.8)
diff1 = np.zeros(len(xvals1))
diff2 = np.zeros(len(xvals1))
n = np.arange(800,800+len(xvals1)-2)
for i in np.arange(1,len(xvals1)-1):
    diff1[i] = abs(xvals1[i+1]-xvals1[i])
    diff2[i] = abs(xvals2[i+1]-xvals2[i])
diff1 = diff1[1:-1]
diff2 = diff2[1:-1]
plt.figure(figsize=(10,10))
plt.semilogy(n,diff1,label='3.3')
plt.semilogy(n,diff2,label='3.8')
plt.title('Population Values vs Iteration Number')
plt.xlabel('iteration')
plt.ylabel('absolute difference between iterations')
plt.legend()
plt.savefig('part1point2.pdf')
plt.close()
'''
'''
#part1
n = np.arange(1,100)
i=0
for ratio in (0.5,2.8,3.3,3.5,3.8,3.828427):
    plt.figure()
    plt.plot(n,justx(ratio),'b')
    plt.title('Part 1.1 for ratio = {:.4f}'.format(ratio))
    plt.xlabel('iteration')
    plt.ylabel('population')
    plt.savefig('part1point1_{:d}.pdf'.format(i))
    plt.close()
    i+=1
'''