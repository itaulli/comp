import numpy as np
from pylab import *
import scipy.integrate as si

x_dim = 2**7+1
y_dim = 2**7+1
hx = 1.0*x_dim
hy = 1.0*y_dim

def fun(x,i):
    return 100.0*np.sin(i*np.pi*x/hy)

def get_c(i):
    a, b = si.quad(fun, 0, hy, args=(i,))
    return a

constants = np.zeros(125)
for i in range(constants.size):
     constants[i] = (2.0/(hy*np.sinh((i+1)*np.pi*(-hx)/hy)))*get_c(i+1)

def solution(x,y):
    output = 0
    for i in range(len(constants)):
        output += constants[i]*np.sinh((i+1)*np.pi*(x-hx)/hy)*np.sin((i+1)*np.pi*y/hy)
    return output

result = np.zeros((y_dim,x_dim))
for i in range(result.shape[0]):
    for j in range(result.shape[1]):
        result[i,j] = solution(j,i)

result[0,:] = 0
result[-1,:] = 0
result[:,-1] = 0
result[:,0] = 100.0

# Plot the grid values using a color map
fig = figure()
ax = fig.add_subplot(111)
mshow = ax.matshow(result)
ax.set_xlabel('Array column number')
ax.set_ylabel('Array row number')
ax.xaxis.set_label_position('top')
fig.colorbar(mshow, aspect=10)

show()
