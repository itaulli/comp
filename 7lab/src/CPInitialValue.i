// This is the SWIG interface file for various initial value problem
// solvers in the Computational Physics class
%module CPInitialValue

%{
#define SWIG_FILE_WITH_INIT
#define PY_ARRAY_UNIQUE_SYMBOL initialvalue_ARRAY_API
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

%{
#include "CPInitialValueSolver.hh"
#include "LaxAdvectionSolver1d.hh"
#include "WaveSolver2d.hh"
%}

%include "CPInitialValueSolver.hh"
%include "LaxAdvectionSolver1d.hh"

// Constructor of the "WaveSolver2d" class includes an array argument.
// We will map this argument into a numpy array.
%apply unsigned IN_ARRAY1[ANY] { unsigned nPoints[ANY] };
%include "WaveSolver2d.hh"
