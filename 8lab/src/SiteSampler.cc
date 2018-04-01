#include <cassert>
#include <stdexcept>
#include <algorithm>

#include "SiteSampler.hh"

SiteSampler::SiteSampler(const double *probabilities, const unsigned length)
    : cdf_(length)
{
    // Check input arguments
    if (!length) throw std::invalid_argument(
        "In SiteSampler constructor: empty transition matrix");
    assert(probabilities);

    // Use a variable with higher precision for accumulating
    // the sum. This helps with round-off errors.
    long double sum = 0.0L;
    for (unsigned i=0; i<length; ++i)
    {
        if (probabilities[i] < 0.0) throw std::invalid_argument(
            "In SiteSampler constructor: negative probability encountered");
        sum += probabilities[i];
        cdf_[i] = sum;
    }
    const double dsum = sum;
    if (dsum == 0.0) throw std::invalid_argument(
        "In SiteSampler constructor: all probabilities are zero");

    firstNonZero_ = length;
    for (unsigned i=0; i<length; ++i)
    {
        cdf_[i] /= dsum;
        if (firstNonZero_ == length && cdf_[i] > 0.0)
            firstNonZero_ = i;
    }

    for (lastNonZero_ = length - 1; lastNonZero_ > 0U; --lastNonZero_)
        if (cdf_[lastNonZero_] > cdf_[lastNonZero_ - 1U])
            break;
}

unsigned SiteSampler::sample(const double rnd) const
{
    if (!(rnd >= 0.0 && rnd <= 1.0)) throw std::domain_error(
        "In SiteSampler::sample: input argument must be between 0 and 1");

    if (rnd == 0.0)
        return firstNonZero_;
    else if (rnd == 1.0)
        return lastNonZero_;
    else
        // Find such j that cdf_[j-1] < rnd <= cdf_[j]
        return std::lower_bound(cdf_.begin(), cdf_.end(), rnd) - cdf_.begin();
}
