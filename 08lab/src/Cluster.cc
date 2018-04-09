#include <cassert>
#include <stdexcept>
#include <cmath>

#include "Cluster.hh"

#define PY_ARRAY_UNIQUE_SYMBOL dla_ARRAY_API
#define NO_IMPORT_ARRAY

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include "numpy/arrayobject.h"

#define idx(i, j) ((i)*static_cast<unsigned long>(size_) + (j))

// sets all the values of a square array to zero and fills 
// the cell in the center of the grid

Cluster::Cluster(const unsigned size, const unsigned nBuffers) 
    : size_(size), result_(0), memory_(0), nBuffers_(nBuffers)
{
    counter_ = 1;
    
    const unsigned long len = arrLen()*nBuffers;
    if (len)
    {
        memory_ = new double[len];
    
    const unsigned long bufLen = arrLen();
    for (unsigned long i=0; i<bufLen; ++i)
    {
        memory_[i] = 0.0;
    }
        result_ = getMemoryBuffer(0);
        halfsize_ = size_/2;
        result_[idx(halfsize_, halfsize_)] = 1.0;
    }
}

Cluster::~Cluster()
{
    delete [] memory_;
}

PyObject* Cluster::convert(const bool reverseRowNumbers) const
{
    // If we do not have the result yet, we can't do anything useful
    if (!result_)
    {   
        throw std::runtime_error("Please calculate the result "
                                 "before attempting to convert it");
        return 0;
    }
    
    // Define the dimensions of the numpy array
    npy_intp array_dim[2];
    array_dim[0] = size_;
    array_dim[1] = size_;
    
    // Note that the code below (in particular, the row reordering
    // functionality) works for 2-d arrays only
    PyObject* array = PyArray_SimpleNew(2, array_dim, NPY_DOUBLE);
    if (array)
    {   
        double* ad = (double*)(PyArray_DATA((PyArrayObject*)array));
        if (reverseRowNumbers)
        {   
            // Need to swap the rows
            for (unsigned row=0; row<size_; ++row)
            {   
                double* buf = result_ + idx(size_-1-row, 0);
                for (unsigned col=0; col<size_; ++col)
                    *ad++ = *buf++;
            }
        }
        else
        {   
            // Can copy elements sequentially
            const unsigned long length = arrLen();
            for (unsigned long i=0; i<length; ++i)
                ad[i] = result_[i];
        }
    }
    return array;
}

double* Cluster::getMemoryBuffer(const unsigned bufferNumber) const
{
    assert(bufferNumber < nBuffers_);
    return memory_ + arrLen()*bufferNumber;
}

bool Cluster::isNear(int i, int j)
{
    if (dist(i,j) < halfsize_ - 1)
    {
        if (result_[idx(i+1, j)] != 0.0) {return true;}
        else if (result_[idx(i-1, j)] != 0.0) {return true;}
        else if (result_[idx(i, j+1)] != 0.0) {return true;}
        else if (result_[idx(i, j-1)] != 0.0) {return true;}
        else {return false;}
    }
    else {return false;}
}

bool Cluster::isFilled(int i, int j)
{
    if (result_[idx(i,j)] != 0.0) {return true;}
    else {return false;}
}

bool Cluster::setCellValue(int i, int j)
{
    if (i < 0 || i >= static_cast<int>(size_)) {return false;}
    if (j < 0 || j >= static_cast<int>(size_)) {return false;}
    if (result_[idx(i, j)]) {return false;}

    result_[idx(i, j)] = ++counter_;
    
    const double R = dist(i, j);
    currentR_ = (R > currentR_) ? R:currentR_;
    return true;
}











