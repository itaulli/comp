"""
Created: Mon Apr 16 18:42:19 2018
Author: Ian Taulli
Description: Two Dimensional Gauss-Seidel Relaxation proceadure for Poisson 
             equation with fixed boundary conditions
"""
import numpy as np

def GSrelax(v, rhs, iteration_limit=1):
    """
    GSrelax(initial_guess, rhs=0, iteration_limit=1)
    
    initial_guess: a 2d array of values representing the solution
    
    rhs: a 2d array of values representing the source charges, defaults 
         to zero (Laplace equation)
    
    interation_limit: an integer, the number of iterations to preform
                      before ending the relaxation, defaults to 1
    """

    n_row,n_col = v.shape
    h_row,h_col = 1.0/n_row, 1.0/n_col
    
    #each entry in the rhs must be multiplied by the differential lengths
    factor = h_row*h_col*rhs
    
    #cycle through the grid, using the updated points as we go
    for iterator in range(iteration_limit):
        for i in range(1, n_row-1):
            for j in range(1, n_col-1):
                v[i,j] = 0.25*(v[i+1,j]+v[i-1,j]+v[i,j+1]+v[i,j-1]+factor[i,j])
    
    return v
