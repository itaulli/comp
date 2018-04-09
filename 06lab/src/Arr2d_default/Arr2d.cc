#include <cassert>
#include <stdexcept>

#include "Arr2d.hh"

// The following two symbols must be defined before
// including "numpy/arrayobject.h" in order for our
// C++ code to be nicely wrapped by SWIG. Note that
// the value of PY_ARRAY_UNIQUE_SYMBOL must be the same
// here and in the Arr2d.i file.
//
// For more details on PY_ARRAY_UNIQUE_SYMBOL, etc, see
// http://docs.scipy.org/doc/numpy/reference/c-api.array.html#importing-the-api
//
#define PY_ARRAY_UNIQUE_SYMBOL arr2d_ARRAY_API
#define NO_IMPORT_ARRAY

// See http://docs.scipy.org/doc/numpy-dev/reference/c-api.deprecations.html
// if you want to understand the meaning of the following #define
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

// The header file for numpy arrays
#include "numpy/arrayobject.h"


// The following macro converts a 2-d array index into a linear index.
// The reason why this index mapping (from 2-d to linear) is needed at all
// is that C++ does not explicitly support multidimensional arrays whose
// dimensions are determined at run time (as opposed to compile time).
// Note that the index will have the type "unsigned long" rather than
// "unsigned". This is needed because a product of two unsigned numbers
// can be larger than the largest unsigned number. Note that the largest
// "unsigned long" is guaranteed to be at least as large as the memory
// available on your machine, so that for array indexing we never need
// to use a type with a larger range than that of "unsigned long".
#define idx(i, j) ((i)*static_cast<unsigned long>(ncols_) + (j))


Arr2d::Arr2d(const unsigned nr, const unsigned nc, const unsigned nBuffers)
    : result_(0), nrows_(nr), ncols_(nc), memory_(0), nBuffers_(nBuffers)
{
    // Allocate the memory of the needed size
    const unsigned long len = arrLen()*nBuffers;
    if (len)
        memory_ = new double[len];
}


Arr2d::Arr2d(const double* existingData, const unsigned nr, const unsigned nc,
             const unsigned nBuffers)
    : result_(0), nrows_(nr), ncols_(nc), memory_(0), nBuffers_(nBuffers)
{
    const unsigned long len = arrLen()*nBuffers;
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


Arr2d::~Arr2d()
{
    // Deallocate the memory that was allocated in the constructor
    delete [] memory_;
}


double Arr2d::GS(double* input)
{
    double* grid0_;
    grid0_ = new double[len];
    const unsigned long bufLen = arrLen();
    for (unsigned long i=0; i<bufLen; ++i) 
        {grid0_[i] = input[i];}
    
    double* grid1_;
    grid1_ = new doulbe[len];
    grid1_ = getMemoryBuffer(1);

    for (unsigned row=0; row<nrows_; ++row) {
        for (unsigned col=0; col<ncols_; ++col) {
            if (grid0_[idx(row,col)] != 0 && grid0_[idx(row,col)] != 100.0 && grid0_[idx(row,col)] != -100.0) {
                grid1_[idx(row,col)] = 0.25*(grid0_[idx(row-1,col)] + grid0_[idx(row,col-1)] + grid0_[idx(row+1,col)] + grid0_[idx(row,col+1)]);
    }}}
    return grid1_;
}

void Arr2d::SOR(int N, double w) : Niter_(N), omega_(w)
{
    double* SOR0_;
    SOR0_ = new double[len];
    double* SOR1_;
    SOR1_ = new doulbe[len];
    SOR0_ = result_;
    SOR1_ = getMemoryBuffer(1);
    for (int n=0; n<Niter_; ++n) {
        GS_ = Arr2d.GS(SOR0_);
        for (unsigned row=0; row<nrows_; ++row) {
            for (unsigned col=0; col<ncols_; ++col) {
                if (SOR0_[idx(row,col)] != 0 && SOR0_[idx(row,col)] != 100.0 && SOR0_[idx(row,col)] != -100.0) {
                    SOR1_[idx(row,col)] = SOR0_[idx(row,col)] + omega_ * (GS_[idx(row,col)] - SOR0_[idx(row,col)]);
    }}}
        SOR0_ = SOR1_;
    }
    result_ = SOR0_;
}


// The following function sets the array values a[i][j] to i*ncols + j*j.
void Arr2d::exampleCalculate()
{
    result_ = getMemoryBuffer(0);
    for (unsigned row=0; row<nrows_; ++row)
        for (unsigned col=0; col<ncols_; ++col)
            result_[idx(row, col)] = row*ncols_ + col*col;
}


// The following function makes a numpy array out of the internal data
PyObject* Arr2d::convert(const bool reverseRowNumbers) const
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


double* Arr2d::getMemoryBuffer(const unsigned bufferNumber) const
{
    assert(bufferNumber < nBuffers_);
    return memory_ + arrLen()*bufferNumber;
}
