"""
Created: Mon Apr 16 18:45:42 2018
Author: Ian Taulli
Description: different multigrid solution schemes
"""
import numpy as np
from MGtools import *
from MGrelax import *

def Vcycle(v, rhs=0, n_relax=3):
    """
    Vcycle(initial_grid, source_grid, limit=False, n_relax=3)
    
    initial_grid: a 2d array of points, your guess at the solution

    source_grid: a 2d array, the right-hand side of Au=f

    n_relax: the number of relaxations to do at each step of the cycle
    """
    if(type(rhs) != int):
        assert(v.shape == rhs.shape), "input grids must have the same shape"
    else:
        rhs = np.zeros(v.shape)

    #setup the grids
    grid = Grid(v, rhs)
    
    #some functions to make the code easier to read
    def sg(i,j,array):
        grid.set_grid(i,j,array)

    def gg(i,j):
        return grid.get_grid(i,j)

    n_grids = grid.num_grids()

    #do the initial relaxations
    sg(0,0, GSrelax(gg(0,0), gg(0,1), n_relax))
    
    #do the restriction loop
    for i in range(1,n_grids-2):
        sg(i,1, restrict(residual(gg(i-1,0), gg(i-1,1))))
        sg(i,0, GSrelax(gg(i,0), gg(i,1), n_relax))

    #do the direct solution on the 3x3 grid
    sg(n_grids-1,1, restrict(residual(gg(n_grids-2,0),gg(n_grids-2,1))))
    C = gg(n_grids-1,1)
    A = (1/C.size)*np.array([[0,1,0],[1,-4,1],[0,1,0]])
    sg(n_grids-1,0, np.linalg.solve(A,C))

    #do the interpolation loop
    for i in np.arange(n_grids-2,-1,-1):
        sg(i,0, gg(i,0)+interpolate(gg(i+1,0)))
        sg(i,0, GSrelax(gg(i,0), gg(i,1), n_relax))

    return gg(0,0)
