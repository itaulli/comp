"""
Created: Wed Feb  7 21:10:00 2018
Author: Ian Taulli
Description:
"""
import numpy as np
import matplotlib.pyplot as plt

#!/usr/bin/env python

from cpode import *
from cpforces import *
from pylab import *
from RK2 import *
from part2force import *
from part2functions import *
import math
import numpy as np

# Prepare the force acting on the test mass (m = 1.0)
power = 2.0
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
odeSolvers = (EulerSolver, EulerCromer, RK2, RK4, RK6)
solvercolor = ('r', 'b', 'g', 'm', 'c', 'b')

# Run for a set of different time deltas.
# We will display them using different colors.
# Run "help(colors)" at the prompt to see
# the inctructions on the use of colors.
timedeltas = np.linspace(1e-6,1e-2,10)

# Cycle over the ODE algorithms
for algorithm in odeSolvers:
    solver = algorithm(force)
    energy_array = []
    coord_array = []

    # Cycle over time deltas and corresponding colors
    for dt in timedeltas:
        # Run the simulation
        solver.run(x0, v0, dt, TimeLimit(timeLimit))
        SolverError = Error(power, sping_constant, x0, v0, solver.x, solver.v, solver.t)
        energy_error = SolverError.EnergyError()
        coord_error = SolverError.CoordError()
        energy_array = energy_array.append(energy_error)
        coord_array = coord_array.append(coord_error)
    
plt.loglog(timedeltas, energy_array, linewidth=1.0, color=color)
    

# Display the results
show()
