#include "Simulation.hh"

Simulation::Simulation(unsigned size, int TransitionMatrix) : size_(size), probtype_(TransitionMatrix)
{
    Cluster = Cluster(size_);
    halfsize_ = size_/2;
    maxR_ = 0.4*size_;
    Cluster.currentR_ = 0.0;
    PI_ = 3.14159;
    counter_ = 2.0;
}

double Simulation::distance(int i, int j)
{
    double square1 = (halfsize_ - i)*(halfsize_ - i);
    double square2 = (halfsize_ - j)*(halfsize_ - j);
    return sqrt(square1 + square2);
}

void Simulation::walk()
{

Seed:

    if(Cluster.currentR_ <= maxR_)
    {
        startingPhi_ = 2.0*PI_*CPP11Random();
        startingR_ = 2.0*(Cluster.currentR_ + maxR_);
        startingI_ = halfsize_ + static_cast<int>(startingR_*sin(startingPhi_));
        startingJ_ = halfsize_ + static_cast<int>(startingR_*cos(startingPhi_));
        walker = Walker(startingI_, startingJ_, probtype_);
        distance_ = startingR_;
        
        while (distance_ <= 4.0*(Cluster.currentR_ + maxR_))
        {
            walker.step();
            distance_ = distance(walker.currentI_, walker.currentJ_);
            if (distance_ < halfsize_ - 2)
            {
                if(Cluster.isNear(walker.currentI_, walker.currentJ_))
                {
                    Cluster.setCellValue(walker.currentI_, walker.currentJ_, counter_);
                    counter_ += 1.0;
                    if(distance_ > Cluster.currentR_)
                    {
                        Cluster.currentR_ = distance_;
                    }
                    goto Seed;
                }
            }
        }
    }
}
