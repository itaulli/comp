# Run "ipython"
#
# Then you can execute this file at the prompt like this:
#
# run bike_with_drag.py
#
# This example models one-dimensional motion of a bicycle with constant
# power and quadratic air drag.
#

from pylab import *
from euler import *

# Define the force model
class ForceOnTheBike:
    def __init__(self, bikerPower, dragCoefficient, frontalArea, airDensity):
        self.P = bikerPower
        self.C = dragCoefficient
        self.A = frontalArea
        self.rho = airDensity
    def __call__(self, t, x, v):
        return self.P/v - self.C*self.rho*self.A*v*abs(v)/2.0

# The running condition for the simulation
class TimeLimit:
    def __init__(self, maxTime):
        self.tend = maxTime
    def __call__(self, t, x, v):
        return t < self.tend

# Prepare the Euler solver
C_drag = 0.5
force = ForceOnTheBike(400.0, C_drag, 0.33, 1.2)
mass = 70.0
bikeMotion = EulerSolver(force, mass)

# Initial conditions
x0 = 0.0
v0 = 4.0

# Run for 200 seconds with the time step of 0.1 s
bikeMotion.run(x0, v0, 0.1, TimeLimit(200))

# Plot the resulting velocity
figure()
plot(bikeMotion.t, bikeMotion.v)

# Put a few finishing touches on the plot
title('Bicycle simulation: velocity vs. time')
xlabel('Time (s)')
ylabel('Velocity (m/s)')

# Display the results
show()

# Now, change the "C_drag" value to 0.0 and rerun
