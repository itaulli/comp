from numpy import *
from pylab import *
from Arr2d import *

# Illustrate Arr2d creation from numpy arrays
na = array(((1.5, 2.0, 3.0),
            (4.0, 5.5, 6.0)))
a = Arr2d(na)
if array_equal(na, a.convert()):
    print("Numpy array is identical to the one stored in Arr2d")

# Illustrate internal calculations
a = Arr2d(100, 100)
a.exampleCalculate()
result = a.convert()

# Plot the result using a color map. See the textbook
# for an example plot utilizing a wire frame.
fig = figure()
ax = fig.add_subplot(111)
mshow = ax.matshow(result)
ax.set_xlabel('Array column number')
ax.set_ylabel('Array row number')
ax.xaxis.set_label_position('top')
fig.colorbar(mshow, aspect=10)

show()
