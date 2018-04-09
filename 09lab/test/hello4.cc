// This code illustrates dynamic creation of threads in case the
// number of threads is not known at the compile time.
//
// TTU Computational Physics course (PHYS 4301/5322)
// I. Volobouev
// 02/04/2018

#include <thread>
#include <mutex>
#include <iostream>
#include <string>
#include <vector>

// Header file for the function which figures out a reasonable
// number of threads to run
#include "figureOutNumThreads.hh"

// Header file for the command line parsing facility. See
// http://www.phys.ttu.edu/~igvol/ComputationalPhysics/Tutorials/Tutorial3/command_line.html
#include "CmdLine.hh"

// Class "Hello4" is exactly the same as "Hello3" in the
// hello3.cc example, but with all comments removed.
// You should understand everything inside this class by now.
class Hello4
{
public:
    Hello4(const std::string& message, const unsigned n)
        : message_(message), myNumber_(n) {}

    void operator()() const
    {
        std::lock_guard<std::mutex> mutexGuard(printMutex_);
        std::cout << message_ << " from " << myNumber_ << "!\n";
    }

private:
    static std::mutex printMutex_;

    std::string message_;
    unsigned myNumber_;
};

std::mutex Hello4::printMutex_;

// We are going to run our threads from the following
// function, "run_threads". In this example, the "main"
// function will only be used to parse the command line
// arguments and to decide how many threads to run. This
// approach illustrates "separation of concerns" at the
// level of code entities and makes the code easier to
// develop and to read.
//
// The return value of this function will be returned from
// "main" as the program status.
//
// Currently, we do not intend to use this function anywhere
// outside this file. To let the compiler know this, the
// function is declared "static".
//
// For code with some intent of reuse, class "Hello4",
// function "run_threads", and function "main" would all
// be implemented in separate files. In such a case this
// function would be declared in a header file, implemented
// in a dedicated .cc file, and we would no longer use
// the "static" keyword.
static int run_threads(const unsigned nthreads)
{
    // Since we do not know the number of threads at the
    // time of compilation, we need to use a variable size
    // container store them. It is convenient to use
    // std::vector for this purpose.
    std::vector<std::thread> threads;

    // Prepare to store "nthreads" threads in the container
    threads.reserve(nthreads);

    // Create "nthreads" threads in a cycle and store them.
    // Upon creation, the threads are immediately scheduled
    // for execution.
    //
    // The vector member function call
    //
    // "emplace_back(Hello4("Hello", i))"
    //
    // used below adds a new thread object at the end
    // of the vector. It is equivalent to
    //
    // "push_back(std::thread{Hello4("Hello", i)})".
    //
    // However, "emplace_back" is slighly faster as it
    // avoids a construction of a temporary "std::thread"
    // object. "emplace_back" appeared in the C++11 version
    // of the C++ standard, so older C++ books will not
    // mention it.
    for (unsigned i=0; i<nthreads; ++i)
        threads.emplace_back(Hello4("Hello", i));

    // Wait until all threads are finished. We are using
    // the range-based "for" loop below (appeared in C++11)
    // which works with standard containters.
    for (auto& t : threads)
        t.join();

    // We are done. Return value of 0 means success.
    return 0;
}

int main(int argc, char *argv[])
{
    // Create the command line parser
    CmdLine cmdline(argc, argv);

    // Initialize variables which can be provided on the
    // command line to their default values. The function
    // "figureOutNumThreads" makes a reasonable guess
    // about the number of threads we should run. Please
    // read the code inside "figureOutNumThreads.hh" and
    // "figureOutNumThreads.cc" files in the ../src
    // directory to see what this function is doing.
    unsigned nThreadsTotal = figureOutNumThreads();

    // Parse command line arguments. The short switch "-n"
    // or the long switch "--nthreads" can be used to specify
    // the total number of threads to run. This number will
    // include the main thread, so only positive arguments
    // make sense.
    try {
        cmdline.option("-n", "--nthreads") >> nThreadsTotal;
        if (!nThreadsTotal)
            throw CmdLineError("positive number of threads expected");

        cmdline.optend();
    }
    catch (const CmdLineError& e) {
        std::cerr << "Error in " << cmdline.progname() << ": "
                  << e.str() << std::endl;
        return 1;
    }

    // Run the real job
    return run_threads(nThreadsTotal-1U);
}
