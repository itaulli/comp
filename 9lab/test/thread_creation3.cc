// This code shows how one can call arbitrary member functions of a class
// in a separate thread (the class is no longer a functor).
//
// TTU Computational Physics course (PHYS 4301/5322)
// I. Volobouev
// 02/04/2018

// To use threads, we must include the standard header file <thread>
#include <thread>
#include "runAsync.hh"

// Other standard headers needed for this example
#include <iostream>
#include <stdexcept>
#include <functional>
#include <cassert>

// The following class simulates a broken arithmometer.
// It returns arithmetic results offset by a constant. We will
// run certain member functions of this class in separate threads.
class BrokenArithmometer
{
public:
    // Constructor
    BrokenArithmometer(const int offset)
        : offset_(offset) {}

    // Copy constructor.
    // When a broken arithmometer is copied, it deteriorates
    // even more, increasing the offset.
    BrokenArithmometer(const BrokenArithmometer& r)
        : offset_(r.offset_ + 1) {}

    int add(const int a, const int b) const
    {
        return a + b + offset_;
    }

    int subtract(const int a, const int b, int* result=nullptr) const
    {
        const int c = a - b + offset_;
        if (result)
            *result = c;
        return c;
    }

private:
    int offset_;
};


// Yet another simple function used to illustrate thread creation
static int standaloneAdd(const int a, const int b, int* result)
{
    assert(result);
    *result = a + b;
    return *result;
}


// This is the program code
int main()
{
    const int a = 3;
    const int b = 2;
    const int offset = 1;

    BrokenArithmometer device{offset};

    // We will want to run "add" and "subtract" methods
    // of the BrokenArithmometer in several different ways.
    // Note that, in order to run a method of a class in
    // a thread, one has to pass the arguments to the
    // the thread constructor (or to the "runAsync" function)
    // in the following order:
    //   1) Pointer to a fully qualified name of the method
    //   2) An object of that class, or a reference to such an object
    //   3) All other arguments of the method
    //
    // Also note that it is not possible to extract the returned
    // value of a function from the std::thread object. Instead,
    // the function itself must write the result into some predefined
    // location or, as in the thread_creation1.cc example, modify
    // the object itself.

    // It does not make sense to run the "add" function of the
    // BrokenArithmometer via a simple thread creation because
    // we can't get the result out. However, we can run "subtract"
    // because it also writes the result to a location provided
    // by the pointer argument. In the call below, "device" argument
    // will be passed by value (that is, copied).
    int c1;
    std::thread t1{&BrokenArithmometer::subtract, device, a, b, &c1};

    // Now, pass "device" by reference
    int c2;
    std::thread t2{&BrokenArithmometer::subtract, std::ref(device), a, b, &c2};

    // Run the "add" method of BrokenArithmometer using "runAsync".
    // Here, we will pass the "device" argument by value.
    auto future1 = runAsync(&BrokenArithmometer::add, device, a, b);

    // Run the "add" method again but pass the "device" argument by reference
    auto future2 = runAsync(&BrokenArithmometer::add, std::ref(device), a, b);

    // The final example here illustrates how to construct a thread using
    // a standalone function (not a method of a class). The function name
    // should be given as the first argument of the thread constructor
    // and the function arguments should follow. Again, the function
    // return value will be ignored by the thread, so the function itself
    // must arrange for storing the result somewhere.
    int c3;
    std::thread t3{standaloneAdd, a, b, &c3};

    // Make sure that all threads in this example run to completion
    t1.join();
    t2.join();
    t3.join();
    future1.wait();
    future2.wait();

    // Print all calculated results
    std::cout << "a = " << a << ", b = " << b << '\n'
              << "\nBrokenArithmometer results are:\n"
              << "a - b = " << c1 << " (by value, using std::thread)\n"
              << "a - b = " << c2 << " (by reference, using std::thread)\n"
              << "a + b = " << future1.get() << " (by value, using runAsync)\n"
              << "a + b = " << future2.get() << " (by reference, using runAsync)\n"
              << "\nstandaloneAdd results are:\n"
              << "a + b = " << c3 << '\n';

    // We are done. Return value of 0 means success.
    return 0;
}
