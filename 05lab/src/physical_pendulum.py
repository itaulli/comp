"""
This module implements the force model for the driven nonlinear pendulum
with dissipation
"""

__author__="Igor Volobouev (i.volobouev@ttu.edu)"
__version__="0.4"
__date__ ="Feb 25 2016"

import cpforces
import math

class DrivenPendulum(cpforces.BasicForce):
    """
    This class models driven nonlinear pendulum with dissipation.

    omega0 is the natural frequency of small amplitude oscillations
    of the pendulum without dissipation.

    q is the dissipation coefficient.

    F_D and omegaD are the amplitude and the frequency of the generalized
    driving force.
    """
    def __init__(self, omega0, dissipationCoefficient, F_D, omegaD):
        self.omega0 = omega0
        self.q = dissipationCoefficient
        self.F_D = F_D
        self.omegaD = omegaD
    def __call__(self, t, theta, omega):
        return -self.omega0*self.omega0*math.sin(theta) - self.q*omega + \
               self.F_D*math.cos(self.omegaD*t)

def standard_angle(angle):
    """
    This function converts all angles to the standard range [-Pi, Pi)
    """
    twopi = 2.0*math.pi
    a = angle % twopi
    if a >= math.pi:
        a -= twopi
    return a
