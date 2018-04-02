#include "Walker.hh"

enum{case0=0, case1, case2}

Walker::Walker(int init_i, int init_j, int TransitionMatrix) 
            : currentI_(init_i), currentJ_(init_j), probtype_(TransitionMatrix)
{
    switch (probtype_)
    {
    case case0:
    {
        prob_array = {0.7071, 1.0, 0.7071, 
                        1.0, 0.0, 1.0, 
                      0.7071, 1.0, 0.7071};
        Pxdim_ = 3;    
    }
    case case1:
    {
        prob_array = {0.5657, 1.0, 0.7071, 
                        0.8, 0.0, 1.0, 
                      0.5657, 1.0, 0.7071};
        Pxdim_ = 3;
    }
    case case2:
    {
        prob_array = {0.7071, 0.0, 1.0, 0.0, 0.7071, 
                        1.0, 0.0, 0.0, 0.0, 1.0, 
                      0.7071, 0.0, 1.0, 0.0, 0.7071};
        Pxdim_ = 5;
    }
    }

    sampler = SiteSampler(prob_array);

}

void Walker::step();
{
    site = sampler.sample(CPP11Random());
    currentI_ += (site / Pxdim) - 1;
    currentJ_ += (site % Pxdim) - 1;
}
