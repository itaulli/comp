"""
A few simple functions to assist in setting up initial wave patterns
for 1d wave motion studies
"""

__author__="Igor Volobouev (i.volobouev@ttu.edu)"
__version__="0.1"
__date__ ="Feb 25 2008"

from pylab import *

def gaussian_wave(xcoords, amplitude, mean, sigma):
    """
    Produces a gaussian wave packet with given amplitude,
    mean value, and standard deviation
    """
    return amplitude*exp(-((xcoords - mean)/sigma)**2/2.0)

def triangle_wave(xcoords, amplitude, location, base):
    """
    Produces a triangular wave packet with given amplitude,
    location of the peak, and size of the triangle base
    """
    halfbase = base/2.0
    dx = abs(xcoords - location)
    return amplitude*(dx < halfbase)*(1.0 - dx/halfbase)

def rectangle_wave(xcoords, amplitude, location, width):
    """
    Produces a rectangular (shock) wave packet with given amplitude,
    location of rectangle middle part, and width
    """
    halfwidth = width/2.0
    dx = abs(xcoords - location)
    return amplitude*(dx < halfwidth)
