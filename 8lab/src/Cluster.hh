// The Class which holds data about the cluster

#include "Python.h"

class Cluster
{
public:
    // Constructs a square array representing a 2D grid
    // with the center point filled in to seed the cluster.
    // Comes with a destructor, and the numpy converter.

    Cluster(unsigned size, unsigned NumberOfBuffers = 1);

    void ~Cluster();

    PyObject* convert(bool reverseRowNumbers = true) const;

    // Object called radius that can be read and set

    double current_radius = 0.0;

    // Checks wheter the given location has a filled cell
    // in the four cardinal directions

    bool isNear(int i, int j); 

    //sets the given cell to the given value

    void setCellValue(int i, int j, double value);

protected:

    double* getMemoryBuffer(unsigned bufferNumber) const;

    inline unsigned long arrLen() const
        {return static_cast<unsigned long>(size*size);}

    const unsigned size_;
    double* result_;

private:

    Cluster(const Cluster&);
    Cluster& operator=(const Cluster&);

    double* memory_;
    unsigned nBuffers_;
    int half_size;
};
