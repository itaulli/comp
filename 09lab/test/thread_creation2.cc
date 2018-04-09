// This code shows how to run a simple function in a dedicated thread
// and how to retrive the result upon calculation completion.
//
// TTU Computational Physics course (PHYS 4301/5322)
// I. Volobouev
// 02/04/2018

// To run asyncronous tasks, we will use the "runAsync" function
// defined in the header file "runAsync.hh". It replaces std::async,
// enforcing immediate launch of a new thread.
#include "runAsync.hh"

// Other standard headers needed for this example
#include <iostream>
#include <stdexcept>

// The following function will run in a separate thread
static unsigned long long factorial(const unsigned n)
{
    if (n > 20U)
        // The result will be larger than 2^64
        throw std::invalid_argument("argument is too large");

    unsigned long long f = 1ULL;
    for (unsigned i=2U; i<=n; ++i)
        f *= i;
    return f;
}

// This is the program code
int main()
{
    // Argument of the factorial. You can change it and see what happens.
    const unsigned n = 15;

    // Launch the calculation of the factorial in a separate thread.
    // The first argument of "runAsync" is the name of the function
    // to run. The second argument is passed to that function.
    // The "runAsync" function returns immediately, not waiting
    // for calculation completion. However, it returns an object that,
    // upon calculation completion in the future, can be used to fetch
    // the result.
    //
    // The variable "futureResult" will actually have the type
    // std::future<unsigned long long>. This is because "factorial"
    // function returns unsigned long long. In subsequent code we
    // don't use the type of "futureResult" explicitly, so instead
    // of naming the exact type we can use the convenient "auto"
    // keyword.
    auto futureResult = runAsync(factorial, n);

    // In more realistic situations, we would be doing some
    // other calculations here, perhaps making more threads.

    // To get the result of the factorial calculation, we need
    // to call the "get()" method of the "futureResult" object.
    // Calling "get()" will internally call the "join()" method
    // of the thread running the calculation and will wait for
    // the thread completion. The type of the result returned by
    // "get" will be the same as the type returned by the "factorial"
    // function, that is, unsigned long long.
    const unsigned long long factorial_of_n = futureResult.get();
    std::cout << n << "! = " << factorial_of_n << '\n';

    // We are done. Return value of 0 means success.
    return 0;
}
