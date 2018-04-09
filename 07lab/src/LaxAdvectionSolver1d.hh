#ifndef LAXADVECTIONSOLVER1D_HH_
#define LAXADVECTIONSOLVER1D_HH_

//========================================================================
// LaxAdvectionSolver1d.hh
//
// Class for solving advection equation in 1-d using finite differences
//
// Constructor arguments are:
//   nSpatialPoints -- number of points in the spatial grid
//   c              -- wave speed
//   dt             -- time step
//   dx             -- space step
//   boundaryType   -- boundary condition type: 0 - fixed ends,
//                     1 - periodic boundary, 2 - free ends
//
// I.Volobouev
// 03/16/2016
//========================================================================

#include "CPInitialValueSolver.hh"

class LaxAdvectionSolver1d : public CPInitialValueSolver
{
public:
    LaxAdvectionSolver1d(unsigned nSpatialPoints, double c,
                         double dt, double dx, int boundaryType=1);
    inline virtual ~LaxAdvectionSolver1d() {}

private:
    const double c_;
    const double dt_;
    const double dx_;
    const int boundaryType_;

    virtual void propagate(double* next, const double** previous);
};

#endif // LAXADVECTIONSOLVER1D_HH_
