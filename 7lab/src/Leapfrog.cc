#include <cassert>

#include "Leapfrog.hh"

enum {
    FIXED_BOUNDARY = 0,
    PERIODIC_BOUNDARY,
    FREE_ENDS_BOUNDARY,
    N_BOUNDARY_TYPES
};

Leapfrog::Leapfrog(const unsigned nSpatialPoints,
                   const double c,
                   const double dt,
                   const double dx,
                   const int boundaryType)
    : CPInitialValueSolver(3, &nSpatialPoints, 1),
      c_(c), dt_(dt), dx_(dx), boundaryType_(boundaryType)
{
    assert(nSpatialPoints >= 3);
    assert(dt_ > 0.0);
    assert(dx_ > 0.0);
    assert(boundaryType_ < N_BOUNDARY_TYPES);
}

void Leapfrog::propagate(double* next, const double** previous)
{
    const double *last = previous[1];
    const double *b4last = previous[0];
    const unsigned lengthMinusOne = sizes_[0] - 1;
    const double rho = c_*dt_/dx_;


    switch (boundaryType_)
    {
    case FIXED_BOUNDARY:
    {
        // Assume that the string is fixed at the edges.
        next[0] = last[0];
        for (unsigned j=1; j<lengthMinusOne; ++j)
            next[j] = rho*rho*(last[j+1] - 2.0*last[j] + last[j-1]) + 2.0*last[j] - b4last[j];
        next[lengthMinusOne] = last[lengthMinusOne];
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
            next[j] = rho*rho*(last[jp1] - 2.0*last[j] + last[jm1]) + 2.0*last[j] - b4last[j];
        }
    }
    break;

    case FREE_ENDS_BOUNDARY:
    {
        // Assume a string with free ends
        for (unsigned j=1; j<lengthMinusOne; ++j)
            next[j] = rho*rho*(last[j+1] - 2.0*last[j] + last[j-1]) + 2.0*last[j] - b4last[j];
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
