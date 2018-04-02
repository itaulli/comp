#include "Cluster.hh"
#include "CPP11Random.hh"
#include "Walker.hh"
#include <math.h>

class Simulation
{
public:

    Simulation(unsigned size, int TransitionMatrix);
 
    void walk();
    double distance(int i, int j);

private:

    double PI_;
    double maxR_;
    double startingR_;
    double startingPhi_;
    int startingI_;
    int startingJ_;
    int halfsize_;
    double counter_;
};
