#!/usr/bin/env python
"""
This script animates 2-d wave motion
"""

__author__="Igor Volobouev (i.volobouev@ttu.edu)"
__version__="0.3"
__date__ ="March 16 2016"

import math
from pylab import *
from wave_utils import *
from CPInitialValue import *
import mpl_toolkits.mplot3d as p3

# Parameters of the simulation.
# Number of discretization grid points in the x direction
n_x_points = 100

# Number of discretization grid points in the y direction
n_y_points = 150

# x dimension of a rectangular membrane
membrane_len_x = 10.0

# y dimension of a rectangular membrane
membrane_len_y = 15.0

# Wave speed. Assume that it is the same in both directions.
c = 10.0

# x coordinates of the grid
xcoords = linspace(0.0, membrane_len_x, n_x_points)
dx = xcoords[1] - xcoords[0]

# y coordinates of the grid
ycoords = linspace(0.0, membrane_len_y, n_y_points)
dy = ycoords[1] - ycoords[0]

# Simulation time step
dt = 0.5*abs(dx/c)

# Total number of time steps for the simulation
maxsteps = int(2*membrane_len_x/(c*dt))

# Create the PDE solver. Note that we need to create an array
# of unsigned ints in order to indicate the grid dimensions.
solver = WaveSolver2d(array((n_y_points, n_x_points), 'u4'), c, dt, dx, dy)

# Set up the initial values for the solver.
# Use one of the eigenmodes to get a nice standing
# wave pattern (easy to visualize).
sine_wave_x = sin(2*math.pi/membrane_len_x*xcoords)
sine_wave_y = sin(4*math.pi/membrane_len_y*ycoords)
initial_values = outer(sine_wave_y, sine_wave_x)
solver.setInitialValues(initial_values, 0)
solver.setInitialValues(initial_values, 1)

# Plot for the waveform
ax = figure().add_subplot(111)
im = ax.imshow(initial_values, vmin=-1, vmax=1)
colorbar(im, aspect=10)
title('2-d Wave Equation Solution')
xlabel('X')
ylabel('Y')
timeLabel = figtext(0.01, 0.5, "t = 0 s", fontsize=24)
draw()

# Turn interactive mode on for dynamic updates
ion()

# Cycle the solver for some time and redraw the plot
for i in range(maxsteps):
    solver.step()
    im.set_array(solver.convert())
    t = dt*solver.resultTime()
    timeLabel.set_text("t = %4.2f s" % t)
    pause(1.e-6)

# Turn off the interactive mode
ioff()

# Display the solution at the end of the simulation as
# a wireframe plot that can be interactively rotated
ax = p3.Axes3D(figure())
x, y = meshgrid(xcoords, ycoords)
ax.plot_wireframe(x, y, solver.convert())
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Displacement')
show()
