#include <cassert>
#include <stdexcept>

#include "CPInitialValueSolver.hh"

#define PY_ARRAY_UNIQUE_SYMBOL initialvalue_ARRAY_API
#define NO_IMPORT_ARRAY
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include "numpy/arrayobject.h"

#define MAXDIM 64

CPInitialValueSolver::CPInitialValueSolver(const unsigned nTSteps,
                                           const unsigned* sizes,
                                           const unsigned dim)
    : nTSteps_(nTSteps),
      sizes_(new unsigned[dim]),
      dim_(dim),
      buffers_(new double*[nTSteps]),
      mostRecentResult_(0),
      timeStepCounter_(0)
{
    assert(nTSteps_ > 1);
    assert(dim_);
    assert(dim_ <= MAXDIM);

    bufferSize_ = 1;
    for (unsigned i=0; i<dim; ++i)
        bufferSize_ *= sizes[i];
    assert(bufferSize_);
    memory_ = new double[nTSteps_*bufferSize_];
    for (unsigned i=0; i<dim; ++i)
        const_cast<unsigned*>(sizes_)[i] = sizes[i];
}

CPInitialValueSolver::~CPInitialValueSolver()
{
    delete [] memory_;
    delete [] buffers_;
    delete [] sizes_;
}

void CPInitialValueSolver::updatePointers()
{
    for (unsigned i=0; i<nTSteps_; ++i)
        buffers_[i] = memory_ + ((i + timeStepCounter_) % nTSteps_)*bufferSize_;
}

void CPInitialValueSolver::step()
{
    updatePointers();
    mostRecentResult_ = buffers_[nTSteps_-1];
    propagate(mostRecentResult_, const_cast<const double**>(buffers_));
    ++timeStepCounter_;
}

unsigned CPInitialValueSolver::resultTime() const
{
    if (!mostRecentResult_)
    {
        throw std::runtime_error("Please run at least one solver step");
        return 0;
    }
    return nTSteps_ + timeStepCounter_ - 2;
}

PyObject* CPInitialValueSolver::convert() const
{
    if (!mostRecentResult_)
    {
        throw std::runtime_error("Please run at least one solver step");
        return 0;
    }

    // Define the dimensions of the numpy array
    npy_intp array_dim[MAXDIM];
    for (unsigned i=0; i<dim_; ++i)
        array_dim[i] = sizes_[i];

    // Create the numpy array
    PyObject* array = PyArray_SimpleNew(dim_, array_dim, NPY_DOUBLE);
    if (array)
    {
        double* ad = (double*)(PyArray_DATA((PyArrayObject*)array));
        for (unsigned long i=0; i<bufferSize_; ++i)
            ad[i] = mostRecentResult_[i];
    }
    return array;
}

PyObject* CPInitialValueSolver::setInitialValues(PyObject* inputArray,
                                                 const unsigned timeStepNumber)
{
    // Check the time step number argument
    if (timeStepNumber >= nTSteps_-1)
    {
        PyErr_SetString(PyExc_ValueError, "Time step number is out of range");
        return 0;
    }
    updatePointers();
    double *tobuf = buffers_[timeStepNumber];

    // Check that the size of the input NumPy array
    // is compatible with the solver buffers
    PyArrayObject* a = reinterpret_cast<PyArrayObject*>(inputArray);
    if (static_cast<unsigned long>(PyArray_SIZE(a)) != bufferSize_)
    {
        PyErr_SetString(PyExc_ValueError, "Incompatible array size");
        return 0;
    }

    // Copy the input array data into the internal buffer.
    // Check that the input array is of useable type.
    switch (PyArray_TYPE(a))
    {
    case NPY_FLOAT:
    {
        const float *frombuf = reinterpret_cast<const float*>(PyArray_DATA(a));
        for (unsigned long i=0; i<bufferSize_; ++i)
            *tobuf++ = *frombuf++;
    }
    break;
    case NPY_DOUBLE:
    {
        const double *frombuf = reinterpret_cast<const double*>(PyArray_DATA(a));
        for (unsigned long i=0; i<bufferSize_; ++i)
            *tobuf++ = *frombuf++;
    }
    break;
    default:
        PyErr_SetString(PyExc_ValueError, "Incompatible array type");
        return 0;
    }

    Py_RETURN_NONE;
}
