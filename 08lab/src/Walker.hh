#ifndef WALKER_HH_
#define WALKER_HH_


#include "SiteSampler.hh"

class Walker
{
public:

    Walker(const double* probabilities, unsigned nrows, unsigned ncols);

    void step(double rnd);
    void setPos(int i, int j);
    inline int getI() const {return currentI_;}
    inline int getJ() const {return currentJ_;}
    inline double rmax() const {return rmax_;}
    
private:

    double rmax_;
    int currentI_;
    int currentJ_;
    int nx;
    int ny;
    SiteSampler sample;
};

#endif //WALKER_HH_
