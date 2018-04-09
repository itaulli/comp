#include "Walker.hh"
#include <cmath>

Walker::Walker(const double* probabilities, unsigned nrows, unsigned ncols) 
            : currentI_(0), currentJ_(0), nx(ncols), ny(nrows), sample(probabilities, nrows*ncols)
{
    rmax_ = hypot(ncols, nrows);
}

void Walker::step(const double rnd)
{
    const int site = sample.sample(rnd);
    const int k = site / nx;
    const int m = site % nx;
    currentI_ += (m - nx/2);
    currentJ_ += (k - ny/2);
}

void Walker::setPos(const int i, const int j)
{
    currentI_ = i;
    currentJ_ = j;
}
