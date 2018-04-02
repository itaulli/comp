// This is the SWIG interface file for DLA model simulation
// in the Computational Physics class
%module dla

%{
#define SWIG_FILE_WITH_INIT
#define PY_ARRAY_UNIQUE_SYMBOL dla_ARRAY_API
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
#include "SiteSampler.hh"
#include "CPP11Random.hh"
#include "Cluster.hh"
#include "Walker.hh"
#include "Simulation.hh"
%}

// Constructor of the "SiteSampler" class includes an array argument.
// We will map this argument into a numpy array.
%include "numpy.i"
%numpy_typemaps(double, NPY_DOUBLE, unsigned)
%apply (double* IN_ARRAY1, unsigned DIM1) {(const double* probabilities, unsigned size)};

%include "SiteSampler.hh"
%include "CPP11Random.hh"
%include "Cluster.hh"
%include "Walker.hh"
%include "Simulation.hh"
