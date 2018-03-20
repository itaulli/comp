#include "Python.h"
#include <cassert>
#include <stdexcept>
#include <cassert>
#include <stdexcept>
#include "numpy/arrayobject.h"

#ifndef ARR2D_HH_
#define ARR2D_HH_
#define PY_ARRAY_UNIQUE_SYMBOL arr2d_ARRAY_API
#define NO_IMPORT_ARRAY
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#define idx(i, j) ((i)*static_cast<unsigned long>(ncols_) + (j))



class Arr2d
{
public:

Arr2d(const unsigned nr, const unsigned nc, const unsigned nBuffers) : result_(0), nrows_(nr), ncols_(nc), memory_(0), nBuffers_(nBuffers)
{
    len = arrLen()*nBuffers;
    if (len)
        memory_ = new double[len];
}

Arr2d(const double* existingData, const unsigned nr, const unsigned nc, const unsigned nBuffers) : result_(0), nrows_(nr), ncols_(nc), memory_(0), nBuffers_(nBuffers)
{
    len = arrLen()*nBuffers;
    if (len)
    {   
        // Allocate the memory of the needed size
        memory_ = new double[len];

        // Copy the input array into the first buffer
        assert(existingData);
        const unsigned long bufLen = arrLen();
        for (unsigned long i=0; i<bufLen; ++i)
            memory_[i] = existingData[i];

        // The result will point to the copy of the input data
        result_ = memory_;
    }
}

virtual ~Arr2d()
{
    // Deallocate the memory that was allocated in the constructor
    delete [] memory_;
}

double* GS(double* input)
{
    double* grid0_;
    grid0_ = new double[len];
    const unsigned long bufLen = arrLen();
    for (unsigned long i=0; i<bufLen; ++i)
        {grid0_[i] = input[i];}

    double* grid1_;
    grid1_ = new double[len];
    grid1_ = getMemoryBuffer(1);

    for (unsigned row=0; row<nrows_; ++row) {
        for (unsigned col=0; col<ncols_; ++col) {
            if (grid0_[idx(row,col)] != 0 && grid0_[idx(row,col)] != 100.0 && grid0_[idx(row,col)] != -100.0) {
                grid1_[idx(row,col)] = 0.25*(grid0_[idx(row-1,col)] + grid0_[idx(row,col-1)] + grid0_[idx(row+1,col)] + grid0_[idx(row,col+1)]);
    }}}
    return grid1_;
}

void SOR(int Niter_, double omega_)
{
    double* SOR0_;
    SOR0_ = new double[len];
    double* SOR1_;
    SOR1_ = new double[len];
    double* GS_;
    GS_ = new double[len];

    SOR0_ = result_;
    SOR1_ = getMemoryBuffer(1);
    for (int n=0; n<Niter_; ++n) {
        GS_ = GS(SOR0_);
        for (unsigned row=0; row<nrows_; ++row) {
            for (unsigned col=0; col<ncols_; ++col) {
                if (SOR0_[idx(row,col)] != 0 && SOR0_[idx(row,col)] != 100.0 && SOR0_[idx(row,col)] != -100.0) {
                    SOR1_[idx(row,col)] = SOR0_[idx(row,col)] + omega_ * (GS_[idx(row,col)] - SOR0_[idx(row,col)]);
    }}}
        SOR0_ = SOR1_;
    }
    result_ = SOR0_;
}

// The following function makes a numpy array out of the internal data
PyObject* convert(const bool reverseRowNumbers = false) const
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
    array_dim[0] = nrows_;
    array_dim[1] = ncols_;

    // Note that the code below (in particular, the row reordering
    // functionality) works for 2-d arrays only
    PyObject* array = PyArray_SimpleNew(2, array_dim, NPY_DOUBLE);
    if (array)
    {
        double* ad = (double*)(PyArray_DATA((PyArrayObject*)array));
        if (reverseRowNumbers)
        {
            // Need to swap the rows
            for (unsigned row=0; row<nrows_; ++row)
            {
                double* buf = result_ + idx(nrows_-1-row, 0);
                for (unsigned col=0; col<ncols_; ++col)
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

protected:

double* getMemoryBuffer(const unsigned bufferNumber) const
{
    assert(bufferNumber < nBuffers_);
    return memory_ + arrLen()*bufferNumber;
}

inline unsigned long arrLen() const
        {return static_cast<unsigned long>(nrows_)*ncols_;}

double* result_;
const unsigned nrows_;
const unsigned ncols_;
unsigned long len;

private:

Arr2d(const Arr2d&);
Arr2d& operator=(const Arr2d&);

double* memory_;
unsigned nBuffers_;

};

#endif // ARR2D_HH_
