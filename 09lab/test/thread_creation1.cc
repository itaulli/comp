// This code shows how one can obtain a result from a functor that
// runs in a dedicated thread.
//
// TTU Computational Physics course (PHYS 4301/5322)
// I. Volobouev
// 02/04/2018

// To use threads, we must include the standard header file <thread>
#include <thread>

// Other standard headers needed for this example
#include <iostream>
#include <stdexcept>

// The following class can be used to calculate n! by a thread.
// All the information needed to perform the calculation is passed
// to the functor in the constructor. Upon calculation completion,
// the result can be retrieved using the "getResult" function.
//
// Of course, in general, functors can be used with threads to perform
// arbitrarily complex calculations, and the change of the functor state
// can also be extensive (in the class below only one variable changes).
//
class Factorial
{
public:
    // Constructor
    Factorial(const unsigned n)
        : n_(n), result_(0)
    {
        if (n_ > 20U)
            // The result will be larger than 2^64
            throw std::invalid_argument("argument is too large");
    }

    // This function will be run by a thread
    void operator()()
    {
        // Calculate n_! and save the result in the
        // object variable result_
        unsigned long long f = 1ULL;
        for (unsigned i=2U; i<=n_; ++i)
            f *= i;
        result_ = f;
    }

    // The following functions can be used to examine functor state
    inline unsigned getN() const {return n_;}

    unsigned long long getResult() const
    {
        if (!result_)
            throw std::runtime_error("please run the calculations first");
        return result_;
    }

private:
    unsigned n_;
    unsigned long long result_;
};


// This is the program code
int main()
{
    // Argument of the factorial. You can change it and see what happens.
    const unsigned n = 15;

    // In order to be able to retrieve the result later, we need
    // to create the functor here.
    Factorial factorial(n);

    // It is worth emphasizing that the thread constructor _copies_
    // all of its arguments. Therefore, creating the thread like this:
    // "std::thread t(factorial)", will work not with the "factorial"
    // object we created above but with its copy. This is not helpful
    // because we will not be able to obtain that copy from the thread
    // and, therefore, will not be able to retrieve the calculated result.
    // The solution to this is to pass a reference to the thread, as
    // shown below. The thread constructor will copy the reference, but
    // that copy will still refer to the same functor object.
    //
    // std::ref is declared in the standard header file <functional>.
    std::thread t(std::ref(factorial));

    // In more realistic situations, we would be doing some
    // other calculations here, perhaps making more threads.

    // Wait until the factorial thread runs to completion
    t.join();

    // Retrieve the result. It is important to note that,
    // when a thread terminates, all variables written
    // by that thread are flushed to main memory. This is
    // why we don't need to do anything special in order to
    // see the result produced by "t" from the main thread.
    std::cout << factorial.getN() << "! = " << factorial.getResult() << '\n';

    // We are done. Return value of 0 means success.
    return 0;
}
