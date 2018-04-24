"""
Created: Mon Apr 16 18:32:46 2018
Author: Ian Taulli
Description: various useful functions for multigrid methods
             including: interpolation and restriction
                        application of the differential operator
                        calculation of residual 
"""
import numpy as np

###interpolate and restrict are from Stewart's text###
def interpolate(v):
    pshape = (2*v.shape[0]-1, 2*v.shape[1]-1)
    p = np.zeros(pshape)
    p[0::2,0::2] = v[0:,0:]
    p[1:-1:2,0::2] = 0.5*(v[0:-1,0:]+v[1:,0:])
    p[0::2,1:-1:2] = 0.5*(v[0:,0:-1]+v[0:,1:])
    p[1:-1:2,1:-1:2] = 0.25*(v[0:-1,0:-1]+v[1:,0:-1]+v[0:-1,1:]+v[1:,1:])
    return p

def restrict(v):
    rshape = (v.shape[0]//2+1, v.shape[1]//2+1)
    r = np.zeros(rshape)
    r[1:-1,1:-1] = 0.5*v[2:-1:2,2:-1:2]+0.125*(v[2:-1:2,1:-2:2]+v[2:-1:2,3::2]+v[1:-2:2,2:-1:2]+v[3::2,2:-1:2])
    r[0,0:] = v[0,0::2]
    r[-1,0:] = v[-1,0::2]
    r[0:,0] = v[0::2,0]
    r[0:,-1] = v[0::2,-1]
    return r

def Laplacian(v):
    h2 = 1.0/(v.shape[0]*v.shape[1])
    output = np.zeros(v.shape)
    output[1:-1:2,1:-1:2] = (v[0:-2:2,1:-1:2]+v[2::2,1:-1:2]+v[1:-1:2,0:-2:2]+v[1:-1:2,2::2]-4*v[1:-1:2,1:-1:2])/h2
    output[2:-2:2,2:-2:2] = (v[1:-3:2,2:-2:2]+v[3:-1:2,2:-2:2]+v[2:-2:2,1:-3:2]+v[2:-2:2,3:-1:2]-4*v[2:-2:2,2:-2:2])/h2 
    output[2:-2:2,1:-1:2] = (v[1:-3:2,1:-1:2]+v[3:-1:2,1:-1:2]+v[2:-2:2,0:-2:2]+v[2:-2:2,2::2]-4*v[2:-2:2,1:-1:2])/h2
    output[1:-1:2,2:-2:2] = (v[0:-2:2,2:-2:2]+v[2::2,2:-2:2]+v[1:-1:2,1:-3:2]+v[1:-1:2,3:-1:2]-4*v[1:-1:2,2:-2:2])/h2
    return output


def residual(v,f):
    output = np.zeros(v.shape)
    lhs = Laplacian(v)
    output[:,:] = lhs[:,:] - f[:,:]
    return output

def array_dict(size):
    return {0: np.zeros(size), 1: np.zeros(size)}
        
def check_size(size):
    allowed = [2**i+1 for i in range(1,13)] 
    if(size in allowed):
        return True
    else:
        return False
    
class Grid:

    def __init__(self, v, f):

        self.lhs = v
        self.rhs = f

        self.n_row, self.n_col = self.lhs.shape
        assert(check_size(self.n_row) and check_size(self.n_col)), "size not allowed, both dimensions must be of the form 2**n+1"
        self.sizes = [(self.n_row, self.n_col), ]

        while(self.n_row > 3 and self.n_col > 3):
            self.n_row = self.n_row//2+1
            self.n_col = self.n_col//2+1
            self.sizes.append((self.n_row, self.n_col))
        
        """
        self.grids = {}
        for i in range(len(self.sizes)):
            self.grids[i] = array_dict(self.sizes[i])
        """
        self.grids = {i: array_dict(self.sizes[i]) for i in range(len(self.sizes))}

        self.grids[0][0] = self.lhs
        self.grids[0][1] = self.rhs

    def get_grid(self, i,j):
        return self.grids[i][j]

    def set_grid(self, i,j,array):
        self.grids[i][j] = array

    def num_grids(self):
        return len(self.sizes)

def SolveEq(rhs):
    a = 1.0/9.0
    mat = np.zeros((3,3,3,3)) 
    #fill all the elements of the identity matrices
    for i in range(3):
        mat[0][1][i][i] = a
        mat[1][0][i][i] = a
        mat[1][2][i][i] = a
        mat[2][1][i][i] = a
    #fill the elements for the difference matrices
    for i in range(3):
        mat[i][i][0][1] = a
        mat[i][i][1][0] = a
        mat[i][i][1][1] = -4.0*a
        mat[i][i][1][2] = a
        mat[i][i][2][1] = a
    return np.linalg.solve(mat,rhs) 
