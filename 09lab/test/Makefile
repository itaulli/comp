OFILES = ../src/figureOutNumThreads.o

PROGRAMS = deadlock.cc deadlock_fix.cc hello1.cc hello2.cc hello3.cc \
           hello4.cc race.cc race_fix_atomic.cc \
           thread_creation1.cc thread_creation2.cc thread_creation3.cc \
           dinner_and_a_movie.cc race2.cc

# GENFLAGS includes flags common to both the compiler and the linker
GENFLAGS = -std=c++14
INCLUDES = -I../src
CPPFLAGS = $(GENFLAGS) $(INCLUDES) -Wall -W -Werror

LIBS = -lpthread -lm

%.o : %.cc
	g++ -c $(CPPFLAGS) -fPIC -MD $< -o $@
	@sed -i 's,\($*\.o\)[:]*\(.*\),$@: $$\(wildcard\2\)\n\1:\2,g' $*.d

BINARIES = $(PROGRAMS:.cc=)

all: $(BINARIES)

$(BINARIES): % : %.o $(OFILES); g++ $(GENFLAGS) -fPIC -o $@ $^ $(LIBS)

clean:
	rm -f $(BINARIES) core.* *.o *.d ../src/*.o ../src/*.d *~

-include $(OFILES:.o=.d)
-include $(PROGRAMS:.cc=.d)
