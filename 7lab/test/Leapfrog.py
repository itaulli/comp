#!/usr/bin/env python
"""
All the initial values are copied from your file. I used the Advection
solver to get the first step, then used the Leapfrog method to get the
video going.
"""
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

#use advection to get the first step
#boundary_type:
#0->fixed ends
#1->periodic
#2->free ends
boundary_type = 1
solver = LaxAdvectionSolver1d(n_spatial_points, c, dt, dx, boundary_type)

initial_values = triangle_wave(x, 1.0, 3.0, 2.0)
solver.setInitialValues(initial_values)

solver.step()
next_values = solver.convert()

#switch over to the leapfrog method
solver = Leapfrog(n_spatial_points, c, dt, dx, boundary_type)
solver.setInitialValues(initial_values, 0)
solver.setInitialValues(next_values, 1)

# Plot for the waveform
ax = figure().add_subplot(111)
ax.grid(True)
line, = plot(x, initial_values, linewidth=3)
axis([0.0, string_length, -1.2, 1.2])
title('Leapfrog Equation Waveform')
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
