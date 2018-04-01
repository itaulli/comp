#ifndef SITESAMPLER_HH_
#define SITESAMPLER_HH_

//========================================================================
// SiteSampler.hh
//
// A class for sampling sites according to their probabilities.
// This code is agnostic about the spatial structure of the sites:
// the input array of probabilities is assumed to correspond to
// the sequential site numbers. The mapping from multi-d to 1-d
// array and back is up to the user of this class.
//
// I.Volobouev
// 03/10/2014
//========================================================================

#include <vector>

class SiteSampler
{
public:
    // Note that all elements of the "probabilities" array must be
    // non-negative, and at least one of them must be positive.
    // The sum of the probabilities will be normalized to 1 internally.
    // The "size" argument specifies the size of the "probabilities"
    // array, and it must be positive.
    SiteSampler(const double* probabilities, unsigned size);

    // The following function maps a random number between 0 and 1
    // produced by various random number generators into the site number
    unsigned sample(double rnd) const;

    // The following function returns the number of elements in the array
    inline unsigned size() const {return cdf_.size();}

private:
    std::vector<double> cdf_;
    unsigned firstNonZero_;
    unsigned lastNonZero_;
};

#endif // SITESAMPLER_HH_
