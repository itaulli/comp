"""
Created on Thu Feb  1 14:53:51 2018
Author: Ian Taulli
Discription:
"""
import cpode

class RK2(cpode.OdeSolver):
    """
    Implements the 2nd order Runge-Kutta ODE solving scheme.
    """
    _name = "2nd order Runge-Kutta"
    
    def _setup(self):
        self.f = lambda t, x, v: (v, self.Force(t, x, v)/self.mass)
    
    def _step(self, dt, t, x, v):
        halfstep = dt/2.0
        k1x, k1v = self.f(t, x, v)
        k2x, k2v = self.f(t+halfstep, x+halfstep*k1x, v+halfstep*k1v)
        dx = dt*k2x
        dv = dt*k2v
        return dx, dv