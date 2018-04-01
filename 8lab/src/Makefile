#
# Figure out Python-related definitions
#
PYTHON_INCLUDE_DIR = /usr/local/anaconda3/include/python3.6m
NUMPY_INCLUDE_DIR := $(shell python -c "import numpy; print(numpy.get_include())")

OFILES = SiteSampler.o
HFILES = $(OFILES:.o=.hh)

INCLUDES = -I$(PYTHON_INCLUDE_DIR) -I$(NUMPY_INCLUDE_DIR) -I.
OPTIMIZE = -std=c++11 -O
CXX = g++
CXXFLAGS = $(OPTIMIZE) $(INCLUDES) -fPIC -W -Wall

%.o : %.cc
	$(CXX) -c $(CXXFLAGS) -MD $< -o $@
	@sed -i 's,\($*\.o\)[:]*\(.*\),$@: $$\(wildcard\2\)\n\1:\2,g' $*.d

all: _dla.so

_dla.so: dla_wrap.o $(OFILES)
	rm -f $@
	$(CXX) $(OPTIMIZE) -shared -o $@ $^

dla_wrap.cc: dla.i numpy.i $(HFILES)
	rm -f $@
	swig -python -py3 -c++ -o $@ $<

clean:
	rm -fr *.o *.d *.so *~ core.* dla.py dla_wrap.cc __pycache__

-include $(OFILES:.o=.d)
