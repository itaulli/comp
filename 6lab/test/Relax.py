"""
Created: Mon Mar 19 21:50:52 2018
Author: Ian Taulli
Description:
"""
import numpy as np
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from GridFill2d import *
from Arr2d import *

#creates capacitor grid
def Grid(scale):

    assert (scale >= 1 and scale <= 20), "Recommended scales are between 1 and 20" 
    L = 3000*scale
    
    cap_grid = GridFill2d(L, 0.0, 3.0, L, 0.0, 3.0, 5, True)
    assert cap_grid.setRectangle(0.0, 0.0, 3.0, 3.0, 0.0)
    assert cap_grid.setLine(1.0, 1.3, 2.0, 1.3, -100.0)
    assert cap_grid.setLine(1.0, 1.7, 2.0, 1.7, 100.0)
    
    return cap_grid


scale = 1
L = int(3000*scale)

grid0 = np.array(Grid(scale).data)
cpp_grid = Arr2d(grid0, L, L, 2)
cpp_grid.SOR(50, 1.2)
result = cpp_grid.convert()

fig = figure()
ax = fig.add_subplot(111)
mshow = ax.matshow(result)
ax.set_xlabel('Array column number')
ax.set_ylabel('Array row number')
ax.xaxis.set_label_position('top')
fig.colorbar(mshow, aspect=10)
savefig('test.png')
