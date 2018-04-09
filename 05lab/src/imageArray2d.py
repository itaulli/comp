"""
This module implements a simple function which discretizes point
locations into images
"""

__author__="Igor Volobouev (i.volobouev@ttu.edu)"
__version__="0.2"
__date__ ="Feb 25 2016"


from numpy import zeros

def imageArray2d(xSequence, ySequence, nx, xmin, xmax, ny, ymin, ymax):
    """
    This function fills elements which correspond to point locations
    in a 2-d array with ones, for subsequent use with "imshow".
    Function arguments as follows:

    xSequence  -- first coordinates of the points

    ySequence  -- second coordinates of the points

    nx         -- number of cells to use for discretizing the first coordinate
    
    xmin, xmax -- minimum and maximum values of the first coordinate. Points
                  with coordinates outside this range will be ignored.

    ny         -- number of cells to use for discretizing the second coordinate

    ymin, ymax -- minimum and maximum values of the second coordinate. Points
                  with coordinates outside this range will be ignored.
    """
    data = zeros((ny, nx))
    x_image_width = (xmax - xmin)*1.0/nx
    y_image_width = (ymax - ymin)*1.0/ny
    for x, y in zip(xSequence, ySequence):
        ix = int((x - xmin)/x_image_width)
        iy = int((y - ymin)/y_image_width)
        if ix >= 0 and ix < nx and iy >= 0 and iy < ny:
            data[iy][ix] = 1.0
    return data
