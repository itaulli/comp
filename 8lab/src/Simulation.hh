#ifndef SIMULATION_HH_
#define SIMULATION_HH_

#include "Cluster.hh"
#include "CPP11Random.hh"
#include "Walker.hh"

class Simulation
{
public:

    Simulation(double rad_factor, CPP11Random* gen);
 
    bool walk(Walker walker, Cluster* cluster);

private:

    double rfactor_;
    CPP11Random* gen_;
};

#endif //SIMULATION_HH_
