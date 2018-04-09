//========================================================================
// Arr2d.hh
//
// This simple class illustrates creation of numpy arrays from user data.
// The "examplecalculate" function fills the data array with some values,
// and then the "convert" function creates the numpy array of the results.
//
// In addition to serving as a SWIG illustration, this class also manages
// the memory buffers needed to solve the boundary value problems in two
// dimensions. If you inherit your own class from this one, you will not
// have to reimplement that functionality.
//
// I.Volobouev
// 03/04/2016
//========================================================================

#ifndef ARR2D_HH_
#define ARR2D_HH_

#include "Python.h"

class Arr2d
{
public:
    // This constructor creates an uninitialized array.
    //
    // The amount of allocated memory will be nrows*ncols*memoryBuffersNeeded
    // double words. You can derive your own class from "Arr2d" and adjust
    // the argument "memoryBuffersNeeded" according to your needs when you
    // call the constructor of the parent (i.e., this) class. For example,
    // I expect that you will need at least four such buffers to implement
    // a relaxation algorithm: one to hold the data for the current iteration,
    // one for the next iteration, another one to hold the boundary
    // conditions, and yet another for the reference used in convergence
    // determination (if such a reference is available).
    //
    Arr2d(unsigned nrows, unsigned ncols, unsigned memoryBuffersNeeded = 1);

    // This constructor creates an array from some existing data
    Arr2d(const double* existingData, unsigned nrows, unsigned ncols,
          unsigned memoryBuffersNeeded = 1);

    // Destructor (will deallocate the memory used to hold the data)
    virtual ~Arr2d();

    // Fill the array using some internal mechanism. Naturally, when
    // you will be writing such a function for your own class, it will
    // probably have some useful arguments (e.g., the maximum number
    // of iterations allowed, the convergence criterion, the over-relaxation
    // parameter, etc). This function should set the "result_" variable so
    // that it points to the appropriate memory buffer and can later be used
    // by the "convert" method. This function can also return some useful
    // info, for example, the number of iterations actually performed.
    double GS(double* input);
    void SOR();
    void exampleCalculate();

    // Produce a numpy array from the current result. The argument
    // "reverseRowNumbers" allows you to arrange the row numbers
    // (which are typically mapped into y coordinates in color maps)
    // in the reverse order. This can be useful for changing the
    // direction of the y coordinate in the plots (up instead of down).
    //
    // Note the "const" qualifyer at the end of function declaration.
    // This qualifyer tells us that the state of this object is not
    // going to change during execution of this function.
    //
    PyObject* convert(bool reverseRowNumbers = false) const;

protected:
    // Get the memory buffer with the given number. The "bufferNumber"
    // argument should be inside the interval [0, memoryBuffersNeeded).
    double* getMemoryBuffer(unsigned bufferNumber) const;

    // Total length of the array (nrows_ x ncols_). Can be larger
    // than the maximum unsigned number, so use unsigned long.
    inline unsigned long arrLen() const
        {return static_cast<unsigned long>(nrows_)*ncols_;}

    // Convention: class member variables end with underscore.
    // Local variable names utilized in the bodies of the methods
    // do not. If a convention like this is carefully followed,
    // reading the code becomes much easier.
    double* result_;
    const unsigned nrows_;
    const unsigned ncols_;

private:
    // We do not want the compiler to generate the default
    // copy constructor and the assignment operator. The compiler
    // does not know how to make correct, "deep" copy of arrays.
    // Therefore, we will declare these functions but will not
    // define them (any attempt to use these functions will result
    // in a compiling or linking error).
    Arr2d(const Arr2d&);
    Arr2d& operator=(const Arr2d&);

    double* memory_;
    unsigned nBuffers_;
};

#endif // ARR2D_HH_
