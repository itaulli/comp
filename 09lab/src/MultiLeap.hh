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

class MultiLeap : public CPInitialValueSolver
{
public:
    MultiLeap(unsigned nSpatialPoints, double c,
                         double dt, double dx, unsigned nthreads);
    inline virtual ~MultiLeap() {}

private:
    const double c_; 
    const double dt_;
    const double dx_;
    const unsigned nthreads_;
    const unsigned nx_;

    virtual void propagate(double* next, const double** previous);
    int getNext(double* next, const double* last, const double* b4last, unsigned i, 
                    unsigned chunksize_, unsigned nx_, double rho);
};
