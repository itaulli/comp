"""
This module implements a few simple trajectory interpolation methods
for the Computational Physics course
"""

__author__="Igor Volobouev (i.volobouev@ttu.edu)"
__version__="0.1"
__date__ ="Jan 29 2018"


def interpolate_linear(t, t0, x0, t1, x1):
    """
    Linearly interpolate to time t some quantity x with value x0 at
    time t0 and value x1 at time t1
    """
    if t0 > t1:
        t0, x0, t1, x1 = t1, x1, t0, x0
    if t0 == t1 and not x0 == x1:
        raise ValueError("Interpolated quantity can not have two "
                         "different values at the same time")
    if t < t0 or t > t1:
        raise ValueError("Time argument outside of the given interval")
    if t == t0:
        return x0
    if t == t1:
        return x1
    timeDelta = 1.0*(t1 - t0)
    t = (t - t0)/timeDelta
    onemt = 1.0 - t
    return onemt*x0 + t*x1


def interpolate_Hermite(t, t0, x0, v0, t1, x1, v1):
    """
    Interpolate to time t the position of a particle which had coordinate
    x0 and velocity v0 at a time t0 and coordinate x1 and velocity v0 at
    a time t1 using a third-degree polynomial. For more details on the
    method, consult https://en.wikipedia.org/wiki/Cubic_Hermite_spline
    """
    if t0 > t1:
        t0, x0, v0, t1, x1, v1 = t1, x1, v1, t0, x0, v0
    if t0 == t1 and not x0 == x1:
        raise ValueError("Interpolated quantity can not have two "
                         "different values at the same time")
    if t < t0 or t > t1:
        raise ValueError("Time argument outside of the given interval")
    if t == t0:
        return x0
    if t == t1:
        return x1
    timeDelta = 1.0*(t1 - t0)
    t = (t - t0)/timeDelta
    onemt = 1.0 - t
    h00 = onemt*onemt*(1.0 + 2.0*t)
    h10 = onemt*onemt*t
    h01 = t*t*(3.0 - 2.0*t)
    h11 = t*t*onemt
    return h00*x0 + h10*timeDelta*v0 + h01*x1 - h11*timeDelta*v1
