// SWIG interface file for the "Arr2d" class
%module Arr2d

%{
#define SWIG_FILE_WITH_INIT
#define PY_ARRAY_UNIQUE_SYMBOL arr2d_ARRAY_API
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
%}

// Include the numpy typemaps
%include "numpy.i"

// Need this for correct initialization of numpy array code
%init %{
import_array();
%}

// Convert C++ exceptions into python exceptions
%include exception.i
%exception {
  try {
    $action
  } catch (const std::exception& e) {
    SWIG_exception(SWIG_RuntimeError, e.what());
  }
}

// Make sure we can create Arr2d from 2-d numpy arrays
%apply (double* IN_ARRAY2, int DIM1, int DIM2) {(const double* existingData, unsigned nrows, unsigned ncols)};

// Finally, wrap the Arr2d class
%{
#include "Arr2d.cpp"
%}

%include "Arr2d.cpp"

// Clear replacements of existingData, nrows, ncols.
// This can be useful if we have more files to wrap.
%clear (const double* existingData, unsigned nrows, unsigned ncols);
