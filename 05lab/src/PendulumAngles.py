"""
Created: Thu Mar  1 13:32:04 2018
Author: Ian Taulli
Description:
"""
from physical_pendulum import *
from cpode import *
import numpy as np

def PendulumAngles(thetaInitial, F_D):
    
    # System Parameters
    omega0 = 1.0
    dissipationCoefficient = 0.5
    omegaD = 2.0/3.0
    periodD = 2*np.pi/omegaD
    
    # Prepare the force model
    force = DrivenPendulum(omega0, dissipationCoefficient, F_D, omegaD)

    # Prepare the ODE solver
    pendulum = RK4(force)

    # Initial conditions
    omegaInitial = 0.0

    # Simulation time step
    dt = 0.04

    # Simulation stopping condition
    whenToStop = TimeLimit(400*periodD)

    # Run the simulation
    pendulum.run(thetaInitial, omegaInitial, dt, whenToStop)
    
    period_times = np.arange(200*periodD,400*periodD,periodD)
    period_angle = []
    for t in period_times:
        x, v = pendulum.interpolate(t)
        period_angle.append(standard_angle(x))
          
    return period_angle