#include "Simulation.hh"

Simulation::Simulation(double rad_factor, CPP11Random* gen) : rfactor_(rad_factor), gen_(gen)
{
}

bool Simulation::walk(Walker walker, Cluster* cluster)
{
    while((*cluster).dist(walker.getI(), walker.getJ()) <= rfactor_*((*cluster).getR()+walker.rmax()))
    {
        walker.step((*gen_)());
       
        if((*cluster).dist(walker.getI(), walker.getJ()) <= (*cluster).getSize()/2)
        {
            if((*cluster).isNear(walker.getI(), walker.getJ()))
            {
                (*cluster).setCellValue(walker.getI(), walker.getJ());
                return true;
            }
        }
    }
    
    return false;
}
