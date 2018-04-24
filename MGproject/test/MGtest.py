import numpy as np
from pylab import *
from GridFill2d import *
from MGalgorithms import *
from MGrelax import *
import time

#set the shape of the solution grid
inital_grid = np.zeros((2**7+1,2**7+1))

#set the boundaries equal to some values
inital_grid[0,:] = 0
inital_grid[-1,:] = 0
inital_grid[:,0] = 100
inital_grid[:,-1] = 0

start = time.time()
result = Vcycle(inital_grid, n_relax=3)
#result = GSrelax(inital_grid, np.zeros(inital_grid.shape), 2000)
end = time.time()

# Plot the grid values using a color map
fig = figure()
ax = fig.add_subplot(111)
mshow = ax.matshow(result)
ax.set_xlabel('time = {:.4f} (s)'.format(end-start))
ax.set_ylabel('Array row number')
ax.xaxis.set_label_position('top')
fig.colorbar(mshow, aspect=10)

show()
