#ifndef WAVESOLVER2D_HH_
#define WAVESOLVER2D_HH_

//========================================================================
// WaveSolver2d.hh
//
// Class for solving wave equation in 2-d using finite differences,
// leapfrog scheme. As the leapfrog for the wave equation is
// equivalent to the "standard" second derivative discretization
// (slide 14 in the lecture), it is also called "explicit differencing"
// scheme.
//
// Constructor arguments are:
//   nPoints[2]     -- number of grid rows (x direction) and columns (y)
//   c              -- wave speed
//   dt             -- time step
//   dx             -- grid step in the x direction
//   dy             -- grid step in the y direction
//   boundaryType   -- boundary condition type. This argument is currently
//                     ignored (only the fixed boundary is implemented).
//
// I.Volobouev
// 03/16/2016
//========================================================================

#include "CPInitialValueSolver.hh"

class WaveSolver2d : public CPInitialValueSolver
{
public:
    WaveSolver2d(const unsigned nPoints[2], double c, double dt,
                 double dx, double dy, int boundaryType=0);
    inline virtual ~WaveSolver2d() {}

private:
    const double c_;
    const double dt_;
    const double dx_;
    const double dy_;    
    const int boundaryType_;

    virtual void propagate(double* next, const double** previous);
};

#endif // WAVESOLVER2D_HH_
