# Run "ipython"
#
# Then you can execute this file at the prompt like this:
#
# run projectile_in_vacuum.py

from v3 import *
from pylab import *
from euler import *

# Convention for the coordinates:
#
# x axis is horizontal, along the projectile motion.
# y axis is vertical (directed upwards), and z axis makes
# a left-handed coordinate system with x and y.

# The acceleration model
class AccelerationDueToGravity:
    def __init__(self):
        # Standard acceleration due to free fall is defined by
        # the ISO standard 80000-3
        self.g = V3(0.0, -9.80665, 0.0)
    def __call__(self, t, x, v):
        return self.g

# The running condition for the simulation
class AboveGround:
    def __call__(self, t, x, v):
        return x.y >= 0.0

# Prepare the Euler solver
projectileInVacuum = EulerSolver(AccelerationDueToGravity())

# Initial conditions
x0 = V3(0.0, 0.0, 0.0)
v0 = V3(100.0, 100.0, 0.0)

# Run for a set of different time deltas.
# We will display them using different colors.
# Run "help(colors)" at the prompt to see
# the inctructions on the use of colors.
timedeltas = ( 3,   1,  0.2,  0.01)
plotcolors = ('r', 'g', 'm',   'b')

figure()
text_position = 0.5

# Cycle over time deltas and corresponding colors
for dt, color in zip(timedeltas, plotcolors):
    # Run the simulation
    projectileInVacuum.run(x0, v0, dt, AboveGround())

    # Extract the trajectory in the XY plane
    xcoords = [vector.x for vector in projectileInVacuum.x]
    ycoords = [vector.y for vector in projectileInVacuum.x]

    # Draw the trajectory
    plot(xcoords, ycoords, linewidth=1.0, color=color)

    # Put a label on the plot which shows dt with the same color
    # as the plot line
    text(0.4, text_position, "dt = %s" % dt, color=color,
         transform = subplot(111).transAxes)
    text_position -= 0.1

# Put a few finishing touches on the plot
title('Simulated Trajectories of a Projectile in Vacuum (Euler Method)')
xlabel('X (m)')
ylabel('Y (m)')

# Display the results
show()
