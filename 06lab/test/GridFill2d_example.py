#!/usr/bin/env python
#
# You can get a description of the GridFill2d functionality
# at the interactive python prompt in the usual manner:
#
# from GridFill2d import *
# help(GridFill2d)

from pylab import *
from GridFill2d import *

# Create a GridFill2d object. Of course, for realistic
# calculations you will need a lot more than 61 grid
# points in each direction.
g = GridFill2d(61, -1.5, 1.5, 61, -1.5, 1.5, 2.0, True)

# Use various methods of GridFill2d. The "assert" statements
# ensure that everything we are drawing fits inside the grid.
assert g.setPoint(-0.5, 0.6, 0.0)
assert g.setPoint(0.5, 0.5, 0.0)
assert g.setLine(-0.7, 1.2, -0.2, 1.0, 1)
assert g.setLine(0.2, 1.0, 0.8, 1.0, 1)
assert g.setRectangle(-1.5, -1.5, 1.5, 1.5, 0.0)
assert g.fillRectangle(-0.2, -0.3, 0.0, 0.0, 1)
assert g.setCircle(-0.5, 0.6, 0.3, 1)
assert g.setCircle(0.5, 0.5, 0.3, 1)
assert g.setArc(0.0, 0.0, 0.8, 220, 310, 1)

# Plot the grid values using a color map
fig = figure()
ax = fig.add_subplot(111)
mshow = ax.matshow(g.data)
ax.set_xlabel('Array column number')
ax.set_ylabel('Array row number')
ax.xaxis.set_label_position('top')
fig.colorbar(mshow, aspect=10)

show()
