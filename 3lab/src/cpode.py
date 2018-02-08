"""
This module implements several algorithms for solving particle motion ODEs
for the Computational Physics course. Classes implemented in this file are:

  OdeSolver   -- A base class for solving particle motion ODEs. Runs ODE
                 integration sequences with both constant and adaptive
                 step sizes.

  EulerSolver -- Implements the Euler ODE solving scheme.

  EulerCromer -- Implements the Euler-Cromer ODE solving scheme.

  RK4         -- Implements the 4th order Runge-Kutta ODE solving scheme.

  RK6         -- Implements the 6th order Runge-Kutta ODE solving scheme.

  RKF45       -- Implements the 5th order Runge-Kutta-Fehlberg ODE integration
                 method with an embedded 4th order Runge-Kutta scheme. Can be
                 used with an adaptive step size adjustment.

  TimeLimit   -- A running condition for use with either "run" or "evolve"
                 method of the OdeSolver class and all classes derived from
                 OdeSolver. Stops ODE integration when a predefined time
                 limit is exceeded.

  AboveGround -- Stops ODE integration when the y coordinate of a particle
                 becomes negative.
"""

__author__="Igor Volobouev (i.volobouev@ttu.edu)"
__version__="0.7"
__date__ ="Jan 31 2018"

import math
from bisect import bisect_right
from interpolate import interpolate_linear, interpolate_Hermite

# Follow the "Don't Repeat Yourself" principle. Put the common interface
# definitions together with the common code into the base class.
class OdeSolver:
    """
    Base class for particle motion ODE solving schemes. The subclasses
    must implement the following function:

    _step(self, dt, t, x, v) should return a tuple dx, dv which are
    the coordinate and velocity increments for evolving from the current
    step to the next. Alternatively, if an adaptive step size integration
    is desired, this function can return the tuple dx, dv, errX, errV
    where errX and errV are the scalars estimating the errors in coordinate
    and velocity steps, respectively. In this case the subclass must also
    implement the method _order(self), returning expected order of errors
    (the n in in O(dt^n) precision of the algorithm).

    Also, the subclasses must define the class variable _name which
    should be set to a descriptive string naming the method.

    The subclasses may also provide the function _setup(self) which can
    be used for additional initialization.
    """
    def __init__(self, F, m=1.0):
        self.Force = F
        self.mass = m*1.0
        if (self.mass <= 0.0):
            raise ValueError("Photons and exotic matter are not supported")
        # Variables that can be checked once the simulation is completed
        self.x0 = None
        self.v0 = None
        self.t = None
        self.x = None
        self.v = None
        self.estimatesErrors = None
        self.adaptiveStepSize = None
        self.absTolX = None
        self.relTolX = None
        self.absTolV = None
        self.relTolV = None
        self.stepsMade = None
        self.stepsRejected = None
        # Some parameters for step size adjustments
        self.stepIncreaseTrigger = 0.5
        self.maxStepFactor = 10.0
        self.minStepFactor = 0.2
        self.smallestDecrease = 1.0/math.sqrt(2.0)
        # Run the setup function. Subclasses may be
        # able to do something useful in it.
        self._setup()

    def _setup(self):
        pass

    @classmethod
    def name(cls):
        return cls._name

    # Pythonic convention for implementing "pure virtual"
    # methods is to raise the "NotImplementedError" exception.
    def _step(self, dt, t, x, v):
        raise NotImplementedError("Function not implemented")

    def _order(self):
        raise NotImplementedError("Function not implemented")

    # Check the validity of absolute plus relative tolerance pair
    @staticmethod
    def _checkTol(absTol, relTol):
        if absTol < 0.0 or relTol < 0.0:
            raise ValueError("Tolerances can not be negative")
        if not (absTol > 0.0 or relTol > 0.0):
            raise ValueError("Some tolerances must be positive")

    # The following function will check the validity of arguments
    # given to the "run" or "evolve" methods. It will also call
    # the "_step" function once, in order to figure out whether it
    # provides the error estimates.
    def _validateRunArguments(self, xInitial, vInitial, dt,
                              runningCondition, tolerances):
        # Make sure dt can be converted into a float
        dt = dt*1.0
        # Running the simulation backwards requires special care
        # which is beyond our purposes here
        assert dt > 0.0, "Can not run the simulation backward in time"
        # Remember the initial conditions
        self.x0 = xInitial*1.0
        self.v0 = vInitial*1.0
        self.stepsMade = 0
        self.stepsRejected = 0
        # Figure out if the class estimates the errors
        stepTuple = self._step(dt, 0.0, self.x0, self.v0)
        self.estimatesErrors = len(stepTuple) == 4
        # Unpack the tolerances and check their validity
        self.adaptiveStepSize = False
        self.absTolX = None
        self.relTolX = None
        self.absTolV = None
        self.relTolV = None
        if not (tolerances is None):
            # Providing tolerances only makes sense for ODE schemes
            # with error estimates
            assert self.estimatesErrors, "Can not use tolerances with this ODE scheme"
            if len(tolerances) == 2:
                absTolX, relTolX = tolerances
            elif len(tolerances) == 4:
                absTolX, relTolX, absTolV, relTolV = tolerances
            else:
                raise ValueError("Invalid specification of tolerances")
            if not (absTolX is None):
                self.absTolX = absTolX*1.0
                self.relTolX = relTolX*1.0
                self._checkTol(self.absTolX, self.relTolX)
                self.adaptiveStepSize = True
            if not (absTolV is None):
                self.absTolV = absTolV*1.0
                self.relTolV = relTolV*1.0
                self._checkTol(self.absTolV, self.relTolV)
                self.adaptiveStepSize = True

    # Make a variable time step, adjusting dt as needed
    def _makeVariableSizeStep(self, dt_in, t, x, v):
        errPower = 1.0/(1.0 + self._order())
        optimal_dt = dt_in
        xMagnitude = abs(x)
        vMagnitude = abs(v)
        minStepSizeReached = False
        maxtries = 20

        for itry in range(maxtries):
            dt = optimal_dt
            dx, dv, errX, errV = self._step(dt, t, x, v)

            nTerms = 0
            xRatio = 0.0
            if not (self.absTolX is None):
                tolX = self.absTolX + max(xMagnitude, abs(dx))*self.relTolX
                assert tolX > 0.0
                xRatio = abs(errX)/tolX
                nTerms += 1

            vRatio = 0.0
            if not (self.absTolV is None):
                tolV = self.absTolV + max(vMagnitude, abs(dv))*self.relTolV
                assert tolV > 0.0
                vRatio = abs(errV)/tolV
                nTerms += 1

            eRatio = math.sqrt((xRatio*xRatio + vRatio*vRatio)/nTerms)
            if eRatio <= 1.0:
                # The estimated error is smaller than the requested tolerance.
                # Accept this step. Check if we want to increase the step size.
                if eRatio < self.stepIncreaseTrigger:
                    optimal_dt = dt/pow(eRatio/self.stepIncreaseTrigger, errPower)
                    if optimal_dt/dt_in > self.maxStepFactor:
                        optimal_dt = dt_in*self.maxStepFactor
                break
            else:
                # Reject this step. Decrease the step size.
                if minStepSizeReached:
                    break
                else:
                    sqtrig = math.sqrt(self.stepIncreaseTrigger)
                    optimal_dt = dt/pow(eRatio/sqtrig, errPower)
                    if optimal_dt/dt_in > self.smallestDecrease:
                        optimal_dt = dt_in*self.smallestDecrease
                    if optimal_dt/dt_in < self.minStepFactor:
                        optimal_dt = dt_in*self.minStepFactor
                        minStepSizeReached = True

        assert itry + 1 < maxtries, "Something is wrong with the variabe step tuning"
        return dt, dx, dv, optimal_dt, itry

    # Run the simulation with a constant time step, accumulating the history
    def _runCS(self, dt, runningCondition):
        # Make sure dt is float. Then t will be float as well.
        dt = dt*1.0
        # Initialize the running variables
        t = 0.0
        x = self.x0
        v = self.v0
        nsteps = 0
        # Initialize the history
        tHistory = [t,]
        xHistory = [x,]
        vHistory = [v,]
        # Cycle until the running condition is no longer true
        while (runningCondition(t, x, v)):
            dx, dv = self._step(dt, t, x, v)[:2]
            x = x + dx
            v = v + dv
            # If we were not accumulating the history, the
            # use of += operator would be more appropriate
            # (i.e., x += dx, as used inside _evolveCS method).
            # However, the += operator does not necessarily
            # create a new object (x can be mutable), and we
            # do not want to fill the history with references
            # to the same object! This illustrates, again,
            # the distinction between Python variables and
            # variables in other programming languages.
            #
            # Also, we do not use t += dt (floats are immutable
            # so the comment above does not apply) because this
            # can lead to accumulation of round-off errors. For
            # x and v (or for t in the variable step size method)
            # we have no choice but here we can avoid it.
            nsteps += 1
            t = dt*nsteps
            # Fill the history
            tHistory.append(t)
            xHistory.append(x)
            vHistory.append(v)
        self.stepsMade = nsteps
        return tHistory, xHistory, vHistory

    # Run the simulation with a variable time step, accumulating the history
    def _runVS(self, dt, runningCondition):
        # Initialize the running variables
        dt = dt*1.0
        t = 0.0
        x = self.x0
        v = self.v0
        # Initialize the history
        tHistory = [t,]
        xHistory = [x,]
        vHistory = [v,]
        # Cycle until the running condition is no longer true
        while (runningCondition(t, x, v)):
            dt, dx, dv, next_dt, nreject = self._makeVariableSizeStep(dt, t, x, v)
            t += dt
            x = x + dx
            v = v + dv
            tHistory.append(t)
            xHistory.append(x)
            vHistory.append(v)
            dt = next_dt
            self.stepsMade += 1
            self.stepsRejected += nreject
        return tHistory, xHistory, vHistory

    # Run the simulation with a constant time step without accumulating history
    def _evolveCS(self, dt, runningCondition):
        # Make sure dt is float. Then t will be float as well.
        dt = dt*1.0
        # Initialize the running variables
        t = 0.0
        x = self.x0
        v = self.v0
        nsteps = 0
        # Cycle until the running condition is no longer true
        while (runningCondition(t, x, v)):
            dx, dv = self._step(dt, t, x, v)[:2]
            x += dx
            v += dv
            nsteps += 1
            t = dt*nsteps
        self.stepsMade = nsteps
        return t, x, v

    # Run the simulation with a variable time step without accumulating history
    def _evolveVS(self, dt, runningCondition):
        # Initialize the running variables
        dt = dt*1.0
        t = 0.0
        x = self.x0
        v = self.v0
        # Cycle until the running condition is no longer true
        while (runningCondition(t, x, v)):
            dt, dx, dv, next_dt, nreject = self._makeVariableSizeStep(dt, t, x, v)
            t += dt
            x += dx
            v += dv
            dt = next_dt
            self.stepsMade += 1
            self.stepsRejected += nreject
        return t, x, v

    def run(self, xInitial, vInitial, dt, runningCondition, tolerances=None):
        """
        Performs ODE integration and accumulate the history (i.e., remembers
        the particle trajectory). Arguments are as follows:

        xInitial         -- Initial coordinates
        vInitial         -- Initial velocities
        dt               -- Simulation time step
        runningCondition -- Callable which should return "true" at each
                            step if we are to continue the simulation.
                            It is called as runningCondition(t, x, v).
        tolerances       -- A tuple of tolerances needed for ODE integration
                            with adaptive step size. Should look like (a, b),
                            (a, b, c, d), or None. 
                            a is the tolerance for absolute coordinate errors
                              for one step
                            b is the tolerance for relative coordinate errors
                              for one step
                            c is the tolerance for absolute speed errors
                              for one step
                            d is the tolerance for relative speed errors
                              for one step
                            If this argument is set to None or omitted,
                            a constant time step is used, even if the class
                            supports stepwise error estimation.

        Upon successful completion, the class members t, x, and v will
        contain the list of time stamps, the list of particle coordinates,
        and the list of velocities, respectively.
        """
        self._validateRunArguments(xInitial, vInitial, dt,
                                   runningCondition, tolerances)
        # Choose variable or constant step size
        if self.adaptiveStepSize:
            self.t, self.x, self.v = self._runVS(dt, runningCondition)
        else:
            self.t, self.x, self.v = self._runCS(dt, runningCondition)

    def evolve(self, xInitial, vInitial, dt, runningCondition, tolerances=None):
        """
        Performs ODE integration without accumulating the history.
        Arguments are as follows:

        xInitial         -- Initial coordinates
        vInitial         -- Initial velocities
        dt               -- Simulation time step
        runningCondition -- Callable which should return "true" at each
                            step if we are to continue the simulation.
                            It is called as runningCondition(t, x, v).
        tolerances       -- A tuple of tolerances needed for ODE integration
                            with adaptive step size. Should look like (a, b),
                            (a, b, c, d), or None. 
                            a is the tolerance for absolute coordinate errors
                              for one step
                            b is the tolerance for relative coordinate errors
                              for one step
                            c is the tolerance for absolute speed errors
                              for one step
                            d is the tolerance for relative speed errors
                              for one step
                            If this argument is set to None or omitted,
                            a constant time step is used, even if the class
                            supports stepwise error estimation.

        Upon successful completion, the class members t, x, and v will
        contain the final time, coordinate, and velocity of the particle.
        """
        self._validateRunArguments(xInitial, vInitial, dt,
                                   runningCondition, tolerances)
        # Choose variable or constant step size
        if self.adaptiveStepSize:
            self.t, self.x, self.v = self._evolveVS(dt, runningCondition)
        else:
            self.t, self.x, self.v = self._evolveCS(dt, runningCondition)

    def interpolate(self, t):
        """
        This function can be invoked after calling "run" in order to
        interpolate system coordinates and velocity to an arbitrary time
        moment covered by the simulation. The interpolation is between
        the two history points closest to the given time. The method is
        cubic in coordinates (so that the coordinate interpolation error
        is O(dt^4)) and linear in velocity. Note that, for precision work,
        the interpolation error has to be at least as good as the error
        of the ODE solving scheme. For high order ODE schemes, you should
        not use this function to sample the simulation history at time
        intervals shorter than the simulation time step -- instead, just
        rerun the simulation using a smaller step.
        """
        try:
            n = len(self.t)
        except TypeError:
            # self.t is not a sequence. Re-raise the exception
            # with an appropriate error message.
            raise TypeError("Please run the simulation first")
        else:
            if (n < 2):
                raise ValueError("Not enough simulation steps")
            tmin = self.t[0]
            tmax = self.t[n-1]
            if t < tmin or t > tmax:
                raise ValueError("Requested time is outside the simulated interval")
            if self.adaptiveStepSize:
                nbelow = bisect_right(self.t, t) - 1    
            else:
                dt = (tmax - tmin)*1.0/(n - 1)
                nbelow = int(math.floor((t - tmin)/dt))
            nabove = nbelow + 1
            if nabove >= n:
                nabove = n - 1
                nbelow = nabove - 1
            x = interpolate_Hermite(t, self.t[nbelow], self.x[nbelow], self.v[nbelow],
                                    self.t[nabove], self.x[nabove], self.v[nabove])
            v = interpolate_linear(t, self.t[nbelow], self.v[nbelow],
                                   self.t[nabove], self.v[nabove])
            return x, v

###########################################################################
#
# Some concrete implementations of the base class follow
#
###########################################################################

class EulerSolver(OdeSolver):
    """
    Implements the Euler ODE solving scheme. Construct the solver with
    EulerSolver(F, m) where F is the force model and m is the particle mass.
    The force model is a callable which will be called by the solver like
    this: F(t, x, v).

    It is also possible to call the solver as EulerSolver(A) where A is
    the acceleration as a function of t, x, and v (unit mass is assumed).
    """
    _name = "Euler"

    def _step(self, dt, t, x, v):
        # Euler scheme: x and v are taken at the current t
        dv = self.Force(t, x, v)/self.mass*dt
        dx = v*dt
        return dx, dv


class EulerCromer(OdeSolver):
    """
    Implements the Euler-Cromer ODE solving scheme. Construct the solver with
    EulerCromer(F, m) where F is the force model and m is the particle mass.
    The force model is a callable which will be called by the solver like
    this: F(t, x, v).

    It is also possible to call the solver as EulerCromer(A) where A is
    the acceleration as a function of t, x, and v (unit mass is assumed).
    """
    _name = "Euler-Cromer"

    def _step(self, dt, t, x, v):
        # Note the difference with the Euler method: the value of dx
        # is calculated using the new value of v, not the old one
        dv = self.Force(t, x, v)/self.mass*dt
        dx = (v + dv)*dt
        return dx, dv


class RK4(OdeSolver):
    """
    Implements the 4th order Runge-Kutta ODE solving scheme. Construct the
    solver with RK4(F, m) where F is the force model and m is the particle
    mass. The force model is a callable which will be called by the solver
    like this: F(t, x, v).

    It is also possible to call the solver as RK4(A) where A is the
    acceleration as a function of t, x, and v (unit mass is assumed).
    """
    _name = "4th order Runge-Kutta"
    
    def _setup(self):
        # For simplicity, define a function which combines
        # x and v variables into one tuple
        self._f = lambda t, x, v: (v, self.Force(t, x, v)/self.mass)
    
    def _step(self, dt, t, x, v):
        halfstep = dt/2.0
        k1x, k1v = self._f(t, x, v)
        k2x, k2v = self._f(t + halfstep, x + halfstep*k1x, v + halfstep*k1v)
        k3x, k3v = self._f(t + halfstep, x + halfstep*k2x, v + halfstep*k2v)
        k4x, k4v = self._f(t + dt, x + dt*k3x, v + dt*k3v)
        dx = dt/6.0*(k1x + 2*k2x + 2*k3x + k4x)
        dv = dt/6.0*(k1v + 2*k2v + 2*k3v + k4v)
        return dx, dv


class RK6(OdeSolver):
    """
    Implements the 6th order Runge-Kutta ODE solving scheme. Construct the
    solver with RK6(F, m) where F is the force model and m is the particle
    mass. The force model is a callable which will be called by the solver
    like this: F(t, x, v).

    It is also possible to call the solver as RK6(A) where A is the
    acceleration as a function of t, x, and v (unit mass is assumed).
    """
    _name = "6th order Runge-Kutta"

    def _setup(self):
        # For simplicity, define a function which combines
        # x and v variables into one tuple
        self._f = lambda h, t, x, v: (h*v, self.Force(t, x, v)/self.mass*h)

    def _step(self, dt, t, x, v):
        # Note that the 6th order scheme requires 7 evaluations of the
        # ODE right hand side function. This is the norm for all Runge-Kutta
        # schemes with order above 4: more function evaluations are needed
        # than the order of the scheme (order 7 requires 9 function
        # evaluations, order 8 requires 11, etc).
        sq21 = math.sqrt(21.0)
        kx1, kv1 = self._f(dt, t, x, v)
        kx2, kv2 = self._f(dt, t + dt, x + kx1, v + kv1)
        kx3, kv3 = self._f(dt, t + dt/2.0, x + (3*kx1 + kx2)/8.0, v + (3*kv1 + kv2)/8.0)
        kx4, kv4 = self._f(dt, t + 2*dt/3.0, x + (8*(kx1 + kx3) + 2*kx2)/27.0,
                                             v + (8*(kv1 + kv3) + 2*kv2)/27.0)
        kx5, kv5 = self._f(dt, t + (7-sq21)*dt/14.0, x + (3*(3*sq21-7)*kx1-8*(7-sq21)*kx2+48*(7-sq21)*kx3-3*(21-sq21)*kx4)/392.0,
                                                     v + (3*(3*sq21-7)*kv1-8*(7-sq21)*kv2+48*(7-sq21)*kv3-3*(21-sq21)*kv4)/392.0)
        kx6, kv6 = self._f(dt, t + (7+sq21)*dt/14.0, x + (-5*(231+51*sq21)*kx1-40*(7+sq21)*kx2-320*sq21*kx3+3*(21+121*sq21)*kx4+392*(6+sq21)*kx5)/1960.0,
                                                     v + (-5*(231+51*sq21)*kv1-40*(7+sq21)*kv2-320*sq21*kv3+3*(21+121*sq21)*kv4+392*(6+sq21)*kv5)/1960.0)
        kx7, kv7 = self._f(dt, t+dt, x + (15*(22+7*sq21)*kx1+120*kx2+40*(7*sq21-5)*kx3-63*(3*sq21-2)*kx4-14*(49+9*sq21)*kx5+70*(7-sq21)*kx6)/180.0,
                                     v + (15*(22+7*sq21)*kv1+120*kv2+40*(7*sq21-5)*kv3-63*(3*sq21-2)*kv4-14*(49+9*sq21)*kv5+70*(7-sq21)*kv6)/180.0)
        dx = (9.0*(kx1 + kx7) + 64.0*kx3 + 49.0*(kx5 + kx6))/180.0
        dv = (9.0*(kv1 + kv7) + 64.0*kv3 + 49.0*(kv5 + kv6))/180.0
        return dx, dv


class RKF45(OdeSolver):
    """
    Implements the 5th order Runge-Kutta-Fehlberg method with an embedded 4th
    order Runge-Kutta scheme. Can be used with an adaptive step size adjustment.
    """
    _name = "5th order Runge-Kutta-Fehlberg"

    def _setup(self):
        # For simplicity, define a function which combines
        # x and v variables into one tuple
        self._f = lambda h, t, x, v: (h*v, self.Force(t, x, v)/self.mass*h)

    def _step(self, dt, t, x, v):
        kx1, kv1 = self._f(dt, t, x, v)
        kx2, kv2 = self._f(dt, t+dt/4.0, x + 0.25*kx1, v + 0.25*kv1)
        kx3, kv3 = self._f(dt, t+3*dt/8.0, x + (3*kx1 + 9*kx2)/32.0,
                                           v + (3*kv1 + 9*kv2)/32.0)
        kx4, kv4 = self._f(dt, t+12*dt/13.0, x + (1932*kx1 - 7200*kx2 + 7296*kx3)/2197.0,
                                             v + (1932*kv1 - 7200*kv2 + 7296*kv3)/2197.0)
        kx5, kv5 = self._f(dt, t+dt, x+(439/216.0*kx1-8*kx2+3680/513.0*kx3-845/4104.0*kx4),
                                     v+(439/216.0*kv1-8*kv2+3680/513.0*kv3-845/4104.0*kv4))
        kx6, kv6 = self._f(dt, t+dt/2.0,
                           x+(-8/27.0*kx1+2*kx2-3544/2565.0*kx3+1859/4104.0*kx4-11/40.0*kx5),
                           v+(-8/27.0*kv1+2*kv2-3544/2565.0*kv3+1859/4104.0*kv4-11/40.0*kv5))
        dx4 = 25/216.0*kx1 + 1408/2565.0*kx3 + 2197/4104.0*kx4 - 0.2*kx5
        dv4 = 25/216.0*kv1 + 1408/2565.0*kv3 + 2197/4104.0*kv4 - 0.2*kv5
        dx5 = 16/135.0*kx1 + 6656/12825.0*kx3 + 28561/56430.0*kx4 - 9/50.0*kx5 + 2/55.0*kx6
        dv5 = 16/135.0*kv1 + 6656/12825.0*kv3 + 28561/56430.0*kv4 - 9/50.0*kv5 + 2/55.0*kv6
        return dx5, dv5, abs(dx5 - dx4), abs(dv5 - dv4)

    def _order(self):
        return 4


###########################################################################
#
# Some common running/stopping conditions for the ODE solvers
#
###########################################################################

class TimeLimit:
    def __init__(self, tmax):
        self.tmax = tmax
    def __call__(self, t, x, v):
        return t < self.tmax

class AboveGround:
    def __call__(self, t, x, v):
        return x.y >= 0.0
