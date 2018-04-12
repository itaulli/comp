#include <cassert>

#include "LaxAdvectionSolver1d.hh"

enum {
    FIXED_BOUNDARY = 0,
    PERIODIC_BOUNDARY,
    FREE_ENDS_BOUNDARY,
    N_BOUNDARY_TYPES
};

LaxAdvectionSolver1d::LaxAdvectionSolver1d(const unsigned nSpatialPoints,
                                           const double c,
                                           const double dt,
                                           const double dx,
                                           const int boundaryType)
    : CPInitialValueSolver(2, &nSpatialPoints, 1),
      c_(c), dt_(dt), dx_(dx), boundaryType_(boundaryType)
{
    assert(nSpatialPoints >= 3);
    assert(dt_ > 0.0);
    assert(dx_ > 0.0);
    assert(boundaryType_ < N_BOUNDARY_TYPES);
}

void LaxAdvectionSolver1d::propagate(double* next, const double** previous)
{
    const double *prev = previous[0];
    const unsigned lengthMinusOne = sizes_[0] - 1;
    const double rho = c_*dt_/2.0/dx_;

    // The Lax updating formula was given at the lecture:
    // http://highenergy.phys.ttu.edu/~igv/ComputationalPhysics/Lectures/lecture7.pdf
    //
    // Depending on the boundary type, we need to do
    // different things with the first and the last
    // grid points.
    switch (boundaryType_)
    {
    case FIXED_BOUNDARY:
    {
        // Assume that the string is fixed at the edges.
        next[0] = prev[0];
        for (unsigned j=1; j<lengthMinusOne; ++j)
            next[j] = (prev[j+1] + prev[j-1])/2.0 - rho*(prev[j+1] - prev[j-1]);
        next[lengthMinusOne] = prev[lengthMinusOne];
    }
    break;

    case PERIODIC_BOUNDARY:
    {
        // Assume periodic boundary conditions
        const unsigned length = sizes_[0];
        for (unsigned j=0; j<length; ++j)
        {
            const unsigned jp1 = (j + 1) % length;
            const unsigned jm1 = j ? j - 1 : lengthMinusOne;
            next[j] = (prev[jp1] + prev[jm1])/2.0 - rho*(prev[jp1] - prev[jm1]);
        }
    }
    break;

    case FREE_ENDS_BOUNDARY:
    {
        // Assume a string with free ends
        for (unsigned j=1; j<lengthMinusOne; ++j)
            next[j] = (prev[j+1] + prev[j-1])/2.0 - rho*(prev[j+1] - prev[j-1]);
        next[0] = next[1];
        next[lengthMinusOne] = next[lengthMinusOne-1];
    }
    break;

    default:
        // We should never end up in this part of the code.
        // However, just think what happens if one invents
        // a new boundary type and forgets to update this
        // switch statement...
        assert(!"Incomplete handling of the switch statement");
    }
}
