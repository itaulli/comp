"""
This module implements Euler's algorithm for solving particle motion ODEs.
"""

__author__="Igor Volobouev (i.volobouev@ttu.edu)"
__version__="0.3"
__date__ ="Feb 03 2016"

#
# Note the convention: this module starts with a brief description of its
# functionality using the triple quotes. The standard module attributes
# __author__, __version__, and __date__ are defined as well. The lines of
# code which define classes and functions are immediately followed by
# documentation lines explaining the usage of these classes and functions.
#
# This convention allows you to view some nicely formatted descriptions
# of modules, classes, and functions at run time. For example, you can
# try the following at the "ipython" prompt:
#
# import euler
#
# help(euler)
# help(euler.EulerSolver)
# help(euler.EulerSolver.run)
#

class EulerSolver:
    """
    Implements the Euler ODE solving scheme. Construct the solver with
    EulerSolver(F, m) where F is the force model and m is the particle mass.
    The force model is a callable which will be called by the solver like
    this: F(t, x, v).

    It is also possible to call the solver as EulerSolver(A) where A is
    the acceleration as a function of t, x, and v (unit mass is assumed).
    """
    def __init__(self, F, m=1.0):
        self.Force = F
        self.mass = m*1.0
        #
        # What if the mass is not positive? We will treat this situation
        # as unphysical and will consider non-positive mass arguments
        # as mistakes. The pythonic way to handle problems like this is
        # to raise an exception. This will typically cause program
        # termination, with some meaninful error message printed out.
        # However, it is also possible for the calling code to "catch"
        # an exception and to rectify the problem. See
        #
        # https://docs.python.org/3.5/tutorial/errors.html
        #
        if (self.mass <= 0.0):
            raise ValueError("Photons and exotic matter are not supported")
        self.x0 = None
        self.v0 = None
        self.t = None
        self.x = None
        self.v = None

    def run(self, xInitial, vInitial, dt, runningCondition):
        """
        Run the simulation and accumulate the history. Arguments are as follows:

        xInitial         -- Initial coordinates
        vInitial         -- Initial velocities
        dt               -- Simulation time step
        runningCondition -- Callable which should return "true" at each
                            step if we are to continue the simulation.
                            It is called as runningCondition(t, x, v)

        The history will be accumulated in the member variables t, x, and v.
        """
        self.x0 = xInitial*1.0
        self.v0 = vInitial*1.0
        t = 0.0
        x = self.x0
        v = self.v0
        #
        # An interesting feature -- trailing comma in the list initialization.
        # While this comma is not necessary for lists, it is required for
        # tuples. Note that (t,) is a tuple with one element while (t) is
        # just t. I find it easier to remember that something with a trailing
        # comma is always a sequence. If you want to know more, take a look at
        # https://docs.python.org/3.5/faq/design.html#why-does-python-allow-commas-at-the-end-of-lists-and-tuples
        #
        self.t = [t,]
        self.x = [x,]
        self.v = [v,]
        while (runningCondition(t, x, v)):
            #
            # Euler scheme: x and v are taken at the current t.
            #
            # Note that, in this whole module, only the following
            # three lines of code are specific to the Euler scheme.
            # Everything else is generic, and should also work with
            # a number of other ODE schemes. In the future, we will
            # want to study other ODE solving algorithms, but copying
            # this whole module and replacing just the three lines
            # below would violate the DRY principle. During the next
            # computational lab you will see how this problem can be
            # resolved using class inheritance.
            #
            dv = self.Force(t, x, v)/self.mass*dt
            x = x + v*dt
            v = v + dv
            #
            # If we were not accumulating the history,
            # the use of += operator would be more appropriate,
            # for example x += v*dt. However, the += operator
            # does not necessarily create a new object, and we
            # do not want to fill the history with references
            # to the same object! This illustrates, again,
            # the distinction between Python variables and
            # variables in other programming languages.
            #
            t = t + dt
            self.t.append(t)
            self.x.append(x)
            self.v.append(v)
