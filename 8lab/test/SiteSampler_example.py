#!/usr/bin/env python3
"""
This script illustrates the usage of the SiteSampler class.
You can run this script multiple times and it will generate
a different random walk trajectory every time.
"""

__author__="Igor Volobouev (i.volobouev@ttu.edu)"
__version__="0.4"
__date__ ="Mar 22 2018"

import matplotlib.pyplot as plt
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

nsteps = np.arange(100,1100,100)

# Perform a random walk. Operator "//" is used to perform integer division.
for n in nsteps
    dist_list = []
    mean_vecx = []
    mean_vecy = []
    for i in range(n):
        Walker.step(gen())
        xcoords.append(Walker.getI())
        ycoords.append(Walker.getJ())
    
    for i in range(len(xcoords))
        dist = np.sqrt(xcoords[i]**2+ycoords[i]**2)
        dist_list.append(dist)

    mean_vecx.append(sum(xcoords)/len(xcoords))
    mean_vecy.append(sum(ycoords)/len(ycoords))

plt.figure()
plt.plot(nsteps,dist_list)
ax = plt.gca()
ax.set_title('mean distance')
ax.set_xlabel('number of steps')
ax.set_ylabel('distance')
plt.savefig('distance_plot.pdf')
plt.close()

plt.figure()
plt.plot(mean_vecx, mean_vecy, 'bo')
ax = plt.gca()
ax.set_title('mean displacement vectors (endpoints)')
ax.set_xlabel('mean x component')
ax.set_ylabel('mean y component')
plt.savefig('vector_plot.pdf')
plt.close() 
'''
# Display the trajectory
plot(xcoords, ycoords)
title("Random Walk Trajectory")
xlabel("X")
ylabel("Y")
show()
'''
