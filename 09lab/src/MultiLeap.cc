#include <cassert>
#include <thread>
#include <vector>
#include <algorithm>
#include "MultiLeap.hh"


MultiLeap::MultiLeap(const unsigned nSpatialPoints,
                   const double c,
                   const double dt,
                   const double dx,
                   const unsigned nthreads)
    : CPInitialValueSolver(3, &nSpatialPoints, 1),
      c_(c), dt_(dt), dx_(dx), nthreads_(nthreads), nx_(nSpatialPoints)
{
    assert(nSpatialPoints >= 3);
    assert(dt_ > 0.0);
    assert(dx_ > 0.0);
}

void MultiLeap::propagate(double* next, const double** previous)
{
    const double *last = previous[1];
    const double *b4last = previous[0];
    const unsigned lengthMinusOne = sizes_[0] - 1;
    const double rho = c_*dt_/dx_;
    
    //the number of spatial points to be assigned to each thread
    const unsigned chunksize_ = nx_/nthreads_ + 1;

    //create the thread vector    
    std::vector<std::thread> threads;
    threads.reserve(nthreads_);

    //the endpoints are fixed outside the loop
    next[0] = last[0];

    //start running the threads and join them afterward
    for(unsigned i=0; i<nthreads_; i++)
        {threads.emplace_back(getNext(next, last, b4last, i, chunksize_, nx_, rho));}
    for(auto& t : threads)
        {t.join();}

    next[lengthMinusOne] = last[lengthMinusOne];

}

//function which allows the thread to calculate the next values in its section
int MultiLeap::getNext(double* next, const double* last, const double* b4last, unsigned i, unsigned chunksize_, unsigned nx_, double rho)
{
    //the allowed values of j depend on the thread number, the min/max functions handle the endpoints
    for (unsigned j=std::max(i*chunksize_, 1); j<std::min((i+1)*chunksize_,nx_); j++)
    {
        if(j==0){j=1;}
        next[j] = rho*rho*(last[j+1] - 2.0*last[j] + last[j-1]) + 2.0*last[j] - b4last[j];
    }
    return 0;
}
