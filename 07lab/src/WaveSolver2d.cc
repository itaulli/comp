#include <cassert>

#include "WaveSolver2d.hh"

WaveSolver2d::WaveSolver2d(const unsigned nPoints[2],
                           const double c,
                           const double dt,
                           const double dx,
                           const double dy,
                           const int boundaryType)
    : CPInitialValueSolver(3, &nPoints[0], 2),
      c_(c), dt_(dt), dx_(dx), dy_(dy), boundaryType_(boundaryType)
{
    assert(nPoints[0] >= 5 && nPoints[1] >= 5);
    assert(dt > 0.0);
    assert(dx > 0.0);
    assert(dy > 0.0);
}

// Macro to simplify writing array indices
#define idx(ix, iy) ((iy)*nX + (ix))

void WaveSolver2d::propagate(double* next, const double** u)
{
    // We will assume that the arrays will be displayed
    // row-by-row (that is, the fastest changing index
    // corresponds to the x direction).
    const unsigned long nX = sizes_[1];
    const unsigned nXm1 = nX - 1;
    const unsigned nY = sizes_[0];
    const unsigned nYm1 = nY - 1;
    const double tcsquared = dt_*dt_*c_*c_;

    // Ignore the boundaryType_ value for now and assume
    // that the string is fixed at the edges
    {
        // Process iy = 0 case (boundary)
        for (unsigned ix=0; ix<nX; ++ix)
            next[idx(ix, 0)] = u[1][idx(ix, 0)];

        // Process 0 < iy < nYm1 case
        for (unsigned iy=1; iy<nYm1; ++iy)
        {
            // Process ix = 0 case (boundary)
            next[idx(0, iy)] = u[1][idx(0, iy)];

            // Process 0 < ix < nXm1 case
            for (unsigned ix=1; ix<nXm1; ++ix)
            {
                const unsigned long icenter = idx(ix, iy);
                const double dudx2 = 
                    (u[1][idx(ix-1, iy)] - 2.0*u[1][icenter] + u[1][idx(ix+1, iy)])/dx_/dx_;
                const double dudy2 = 
                    (u[1][idx(ix, iy-1)] - 2.0*u[1][icenter] + u[1][idx(ix, iy+1)])/dy_/dy_;
                next[icenter] = tcsquared*(dudx2 + dudy2) + 2.0*u[1][icenter] - u[0][icenter];
            }

            // Process ix = nXm1 case (boundary)
            next[idx(nXm1, iy)] = u[1][idx(nXm1, iy)];
        }

        // Process iy = nYm1 case (boundary)
        for (unsigned ix=0; ix<nX; ++ix)
            next[idx(ix, nYm1)] = u[1][idx(ix, nYm1)];
    }
}
