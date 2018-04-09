#ifndef CPINITIALVALUESOLVER_HH_
#define CPINITIALVALUESOLVER_HH_

//========================================================================
// CPInitialValueSolver.hh
//
// Base class for solving initial value problems using the method of
// finite differences. Takes care of the grid memory management
// (using, essentially, a circular buffer) and of the Python interface.
// The user of this class should derive from it and implement the
// "propagate" method.
//
// The class constructor arguments are:
//
//   nTSteps  -- the number of time steps in the method used by the
//               PDE solver. For example FTCS and Lax schemes use two
//               steps (the current and the next), leapfrog scheme
//               uses 3 steps, etc.
//
//   dim      -- Dimensionality of the space (time is separate and not
//               included here)
//
//   sizes    -- Numbers of grid points in each dimension
//
// The information provided in the class constructor is made available
// to the derived classes via protected members of the class.
//
// The arguments of the "propagate" method are:
//
//   next     -- Memory buffer for the next time step. The number of
//               doubles in the buffer will be equal to the total number
//               of points in the spatial discretization grid (product
//               of sizes in each dimension). The organization of memory
//               inside the buffer is up to the user. For example, if
//               you have 2d buffer with NX grid points in the x direction
//               and NY grid points in the y direction, it makes sense
//               to have the fastest running index correspond to the
//               x direction (this is how matplotlib plots images).
//               Then grid[iy][ix] is usually mapped into buffer location
//               iy*NX + ix.
//
//   previous -- Memory buffers from previous time steps. previous[0]
//               is the oldest, previous[1] is one step newer, etc.,
//               and previous[nTSteps-2] is the most recent one.
//
// I.Volobouev
// 03/16/2016
//========================================================================

#include "Python.h"

class CPInitialValueSolver
{
public:
    CPInitialValueSolver(unsigned nTSteps, const unsigned* sizes, unsigned dim);
    virtual ~CPInitialValueSolver();

    // The following virtual functions may be overriden if necessary.
    //
    // The function "setInitialValues" expects a numpy array
    // as its "array" argument. Unfortunately, SWIG does not
    // yet know how to wrap a numpy array with arbitrary,
    // dynamic dimensionality. If the dimensionality is known
    // in advance (i.e., at the compile time), it is easier
    // to use explicit C++-style arguments (for example,
    // "double* data, unsigned nx, unsigned ny" for 2-d arrays)
    // and let SWIG perform the proper argument conversion and
    // the array type verification. Here, instead, this verification
    // will be performed inside the "setInitialValues" function.
    //
    // Depending on the PDE and the differencing scheme, you might
    // need to provide either one or two initial conditions. These
    // conditions are given as coordinates, not velocities. For
    // second order equations in time, if you know initial velocities,
    // make one Euler step at the beginning and convert those
    // velocities into coordinates at the next time step.
    //
    virtual PyObject* setInitialValues(PyObject* array, unsigned timeStep=0);

    // The "convert" function should be familiar to you from
    // the "Arr2d" class described in the previous lab. This
    // function converts the result obtained for the last time
    // step of the simulation into a Python numpy array.
    virtual PyObject* convert() const;

    // Make one time step. This function updates the circular
    // buffer pointers and calls the "propagate" function.
    virtual void step();

    // The time of the current result in the units of time step
    unsigned resultTime() const;

protected:
    // Naming convention: class variable names start with
    // small letters and end with underscores. If one follows
    // this convention, it becomes easier to read the code.
    const unsigned nTSteps_;
    const unsigned* const sizes_;
    const unsigned dim_;

private:
    // We do not want the compiler to generate the copy
    // constructor and the assignment operator. The compiler
    // does not know how to make correct, "deep" copy of arrays.
    CPInitialValueSolver(const CPInitialValueSolver&);
    CPInitialValueSolver& operator=(const CPInitialValueSolver&);

    double* memory_;
    double** buffers_;
    double* mostRecentResult_;
    unsigned timeStepCounter_;
    unsigned long bufferSize_;

    void updatePointers();

    // The following function must be provided by the derived classes.
    // It is private because it is not supposed to be called by the
    // users of this class.
    virtual void propagate(double* next, const double** previous) = 0;
};

#endif // CPINITIALVALUESOLVER_HH_
