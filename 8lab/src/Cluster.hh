#ifndef CLUSTER_HH_
#define CLUSTER_HH_
// The Class which holds data about the cluster

#include "Python.h"

class Cluster
{
public:
    // Constructs a square array representing a 2D grid
    // with the center point filled in to seed the cluster.
    // Comes with a destructor, and the numpy converter.

    Cluster(unsigned size, unsigned NumberOfBuffers = 1);

    ~Cluster();

    PyObject* convert(bool reverseRowNumbers = true) const;

    // Checks wheter the given location has a filled cell
    // in the four cardinal directions

    bool isNear(int i, int j);
    bool isFilled(int i, int j); 

    //sets the given cell to the given value

    bool setCellValue(int i, int j);

    inline unsigned long getCounter() const {return counter_;}
    inline double getR() const {return currentR_;}
    inline double dist(int i, int j) const {return hypot(i-halfsize_,j-halfsize_);}
    inline int getSize() const {return size_;}
    
protected:

    double* getMemoryBuffer(unsigned bufferNumber) const;

    inline unsigned long arrLen() const
        {return static_cast<unsigned long>(size_)*size_;}

    const unsigned size_;
    double* result_;

private:

    Cluster(const Cluster&);
    Cluster& operator=(const Cluster&);

    double* memory_;
    unsigned nBuffers_;
    int halfsize_;
    double currentR_;
    unsigned long counter_;
};

#endif //CLUSTER_HH_

