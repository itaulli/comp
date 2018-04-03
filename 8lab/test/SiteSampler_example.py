#!/usr/bin/env python3
"""
This script illustrates the usage of the SiteSampler class.
You can run this script multiple times and it will generate
a different random walk trajectory every time.
"""

__author__="Igor Volobouev (i.volobouev@ttu.edu)"
__version__="0.4"
__date__ ="Mar 22 2018"

from pylab import *
import dla

# Example array of transition probabilities (not normalized)
p = ((0, 0, 1, 2, 1, 0, 0),
     (0, 1, 2, 3, 2, 1, 0),
     (1, 2, 3, 4, 3, 2, 1),
     (2, 3, 4, 0, 4, 3, 2),
     (1, 2, 3, 4, 3, 2, 1),
     (0, 1, 2, 3, 2, 1, 0),
     (0, 0, 1, 2, 1, 0, 0))
a = array(p, 'float')

# ny is the number of rows and nx is the number of columns
ny, nx = a.shape

# Create the sampler
Walker = dla.Walker(a)

# Starting point for the random walk
x, y = 0, 0
xcoords = [x,]
ycoords = [y,]

# Create generator of random numbers
gen = dla.CPP11Random()



# Perform a random walk. Operator "//" is used to perform integer division.
nsteps = 1000
for i in range(nsteps):
    Walker.step(gen())
    xcoords.append(Walker.getI())
    ycoords.append(Walker.getJ())

# Display the trajectory
plot(xcoords, ycoords)
title("Random Walk Trajectory")
xlabel("X")
ylabel("Y")
show()

