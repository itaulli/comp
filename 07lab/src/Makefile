#
# Figure out Python-related definitions (i.e., where the relevant header
# files should be searched for)
#
PYTHON_INCLUDE_DIR = /usr/local/anaconda3/include/python3.6m
NUMPY_INCLUDE_DIR := $(shell python3 -c "import numpy; print(numpy.get_include())")

OFILES = LaxAdvectionSolver1d.o CPInitialValueSolver.o WaveSolver2d.o Leapfrog.o
HFILES = $(OFILES:.o=.hh)

INCLUDES = -I$(PYTHON_INCLUDE_DIR) -I$(NUMPY_INCLUDE_DIR) -I.
OPTIMIZE = -O
CXX = g++
CXXFLAGS = -W -Wall $(OPTIMIZE) $(INCLUDES) -fPIC

%.o : %.cc
	$(CXX) -c $(CXXFLAGS) -MD $< -o $@
	@sed -i 's,\($*\.o\)[:]*\(.*\),$@: $$\(wildcard\2\)\n\1:\2,g' $*.d

all: _CPInitialValue.so

_CPInitialValue.so: CPInitialValue_wrap.o $(OFILES)
	rm -f $@
	$(CXX) $(OPTIMIZE) -shared -o $@ $^

CPInitialValue_wrap.cc: CPInitialValue.i $(HFILES)
	rm -f $@
	swig -python -py3 -c++ -o $@ $<

clean:
	rm -fr *.o *.d *.so *~ core.* CPInitialValue.py \
             CPInitialValue_wrap.cc __pycache__

-include $(OFILES:.o=.d)
