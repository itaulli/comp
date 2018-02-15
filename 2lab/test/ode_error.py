"""
Created: Wed Feb  7 21:10:00 2018
Author: Ian Taulli
Description: plots the error for different ODE solving methods as a function of step size
"""
import matplotlib.pyplot as plt
from cpode import *
from cpforces import *
from RK2 import *
from part2force import *
from part2functions import *
import math
import numpy as np

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
odeSolvers = (EulerSolver, EulerCromer, RK2, RK4, RK6)
colors = ('r', 'b', 'g', 'm', 'c')

timedeltas = np.linspace(1e-5,1e-2,20)

# Cycle over the ODE algorithms
for algorithm, color in zip(odeSolvers, colors) :
    solver = algorithm(force)
    energy_array = []
    coord_array = []

    # Cycle over time deltas and corresponding colors
    for dt in timedeltas:
        # Run the simulation
        solver.run(x0, v0, dt, TimeLimit(timeLimit))
        # Calls the error functions and fills the error lists
        SolverError = Error(power, spring_constant, x0, v0, solver.x, solver.v, solver.t)
        energy_error = SolverError.EnergyError()
        coord_error = SolverError.CoordError()
        energy_array.append(energy_error)
        coord_array.append(coord_error)
    
    # Places the lines on the figures
    print('done with {:s} Method'.format(solver.name()))
    plt.figure('energy')
    plt.loglog(timedeltas, energy_array, linewidth=1.0, color=color, label=solver.name())
    plt.figure('coords')
    plt.loglog(timedeltas, coord_array, linewidth=1.0, color=color, label=solver.name())

# Decorates the figures and saves them as pdf's
plt.figure('energy')
ax = plt.gca()
ax.grid(True)
ax.set_title('Relative Energy Error')
ax.set_xlabel('time delta')
ax.set_ylabel('energy error')
lines = ax.get_lines()
ax.legend(fontsize=5)
plt.savefig('energy_error_p'+str(int(power))+'.pdf')

plt.figure('coords')
ax = plt.gca()
ax.grid(True)
ax.set_title('Absolute Coordinate Error')
ax.set_xlabel('time delta')
ax.set_ylabel('coordinate error')
lines = ax.get_lines()
ax.legend(fontsize=5)
plt.savefig('coordinate_error_p'+str(int(power))+'.pdf')

print('All done! plots saved as pdf\'s')