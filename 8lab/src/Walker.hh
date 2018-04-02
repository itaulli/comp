#include "SiteSampler.hh"
#include "CPP11Random.hh"

class Walker
{
public:

    Walker(int init_i, int init_j, int TransitionMatrix = 0);

    int currentI_;
    int currentJ_;

    void step();

protected:

    double prob_array[];
    int Pxdim_;
};
