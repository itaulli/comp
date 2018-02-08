#!/usr/bin/env python

from cpode import *
from cpforces import *
from pylab import *
from RK2 import *
from part2force import *
from part2functions import *
import math

# Prepare the force acting on the test mass (m = 1.0)
power = 8.0
spring_constant = 1.0
force = Pforce(power, spring_constant)

# Initial conditions
x0 = 0.0
v0 = 1.01

# When do we stop?
if power == 2.0:
    oscillationPeriod = 2.0*math.pi
    timeLimit = 10*oscillationPeriod
elif power == 8.0:
    oscillationPeriod = 5.5
    timeLimit = 10*oscillationPeriod

# The tuple of ODE algorithms that we are going to use
odeSolvers = (EulerSolver, EulerCromer, RK2, RK4)

# Run for a set of different time deltas.
# We will display them using different colors.
# Run "help(colors)" at the prompt to see
# the inctructions on the use of colors.
timedeltas = (1e-4, 1e-5)
plotcolors = ('orange', 'green')

# Cycle over the ODE algorithms
for algorithm in odeSolvers:
    solver = algorithm(force)

    # Make a new plot and turn on the grid on the plot
    ax = figure().add_subplot(111)
    ax.grid(True)

    text_position = 0.03

    # Cycle over time deltas and corresponding colors
    for dt, color in zip(timedeltas, plotcolors):
        # Run the simulation
        solver.run(x0, v0, dt, TimeLimit(timeLimit))

        # Draw the displacement
        plot(solver.t, solver.x, linewidth=1.0, color=color)

        # Put a label on the plot which shows dt with the same color
        # as the plot line
        text(0.05, text_position, "dt = %s" % dt, color=color,
             transform = ax.transAxes)
        text_position += 0.05

    # Put a few finishing touches on the plot for this solver
    title('Simulated Oscillations (%s Method)' % solver.name())
    xlabel('Time (s)')
    ylabel('X (m)')
    
    #calculation for the report
    SolverError = Error(power, spring_constant, x0, v0, solver.x, solver.v, solver.t)
    print(SolverError.EnergyError())
    print(SolverError.CoordError())
    

# Display the results
show()
