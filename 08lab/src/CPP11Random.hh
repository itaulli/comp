#ifndef CPP11RANDOM_HH_
#define CPP11RANDOM_HH_

//========================================================================
// CPP11Random.hh
//
// This class wraps C++ facilities for random number generation into
// a simple old-style generator. Create an object of this class and
// then use that single object throughout your program.
//
// Note that the g++ compiler needs the "-std=c++11" switch in order
// to be able to compile this code.
//
// I.Volobouev
// 03/10/2014
//========================================================================

#include <random>

#include "CPP11RandomWrapper.hh"

class CPP11Random
{
public:
    // Default constructor (without any arguments) will produce a new
    // random sequence every time an object of this class is created
    inline CPP11Random() : wrapper(eng) {std::random_device r; eng.seed(r());}

    // Use a seed if you want the sequence to be repeatable
    inline explicit CPP11Random(unsigned seed) : eng(seed), wrapper(eng) {}

    // This generates a random number on [0, 1)
    inline double operator()() {return wrapper();}

private:
    std::mt19937 eng;
    CPP11RandomWrapper<std::mt19937> wrapper;
};

#endif // CPP11RANDOM_HH_
