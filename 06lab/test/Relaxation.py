"""
Created: Mon Mar 19 21:50:52 2018
Author: Ian Taulli
Description:
"""
import numpy as np
#import matplotlib.pyplot as plt
from pylab import *
from GridFill2d import *

#creates capacitor grid
def Grid(scale):

    assert (scale >= 1 and scale <= 20), "Recommended scales are between 1 and 20" 
    L = 3000*scale
    
    cap_grid = GridFill2d(L, 0, 3, L, 0, 3, 1e10, True)
    assert cap_grid.setRectangle(0, 0, 3, 3, 0.0)
    assert cap_grid.setLine(1, 1.3, 2, 1.3, -100.0)
    assert cap_grid.setLine(1, 1.7, 2, 1.7, 100.0)
    
    return cap_grid

