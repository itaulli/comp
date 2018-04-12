#!/usr/bin/env python
"""
This script solves the advection equation and animates 1-d wave motion
using matplotlib
"""

__author__="Igor Volobouev (i.volobouev@ttu.edu)"
__version__="0.3"
__date__ ="March 16 2016"

from pylab import *
from wave_utils import *
from CPInitialValue import *

# Basic parameters of the simulation
# Number of discretization grid points
n_spatial_points = 200

# Length of the interval
string_length = 10.0

# Wave propagation speed
c = 10.0

# x coordinates of the grid
x = linspace(0.0, string_length, n_spatial_points)
dx = x[1] - x[0]

# Simulation time step
dt_factor = 1.0
dt = dt_factor*abs(dx/c)

# Total number of time steps for the simulation
maxsteps = int(4*(string_length+dx)/(c*dt))

# Create the PDE solver. The following boundary conditions
# could be interesting:
# boundary_type = 0: the string is fixed at the edges
# boundary_type = 1: periodic boundary conditions
# boundary_type = 2: the string is free at the edges
boundary_type = 0
solver = LaxAdvectionSolver1d(n_spatial_points, c, dt, dx, boundary_type)

# Set up the initial values for the solver
initial_values = triangle_wave(x, 1.0, 3.0, 2.0)
# initial_values = rectangle_wave(x, 1.0, 3.0, 2.0)
# initial_values = gaussian_wave(x, 1.0, 3.0, 1.0)
solver.setInitialValues(initial_values)

# Plot for the waveform
ax = figure().add_subplot(111)
ax.grid(True)
line, = plot(x, initial_values, linewidth=3)
axis([0.0, string_length, -1.2, 1.2])
title('Advection Equation Waveform')
xlabel('X')
ylabel('Displacement')
timeLabel = ax.text(0.4, 0.15, "t = 0 s",
                    transform=ax.transAxes, fontsize=24)
draw()

# Turn interactive mode on for dynamic updates
ion()

# Cycle the solver and update the plot. Of course, the time
# in the animation does not proceed at the wall clock rate.
for i in range(maxsteps):
    solver.step()
    line.set_ydata(solver.convert())
    t = dt*solver.resultTime()
    timeLabel.set_text("t = %4.2f s" % t)
    pause(1.e-6)

# Turn interactive mode off and redisplay the plot
# at the end of the simulation
ioff()
show()
