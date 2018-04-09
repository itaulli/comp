// This code shows how to fix a race condition using atomic variables.
//
// TTU Computational Physics course (PHYS 4301/5322)
// I. Volobouev
// 02/04/2018

// To use atomic variables, we must include the standard header file <atomic>
#include <atomic>

#include <thread>
#include <iostream>
#include <vector>
#include <cassert>

#include "figureOutNumThreads.hh"
#include "CmdLine.hh"

// Function to increment a counter. This function
// will be run simultaneously by several threads.
static void incrementCounter(std::atomic<unsigned long>* counter,
                             const unsigned maxCount)
{
    // Assert all arguments passed by pointer
    assert(counter);

    for (unsigned i=0; i<maxCount; ++i)
        // Increment of an atomic integer is an atomic operation,
        // guaranteed to be executed one thread at a time.
        ++*counter;
}

static int run_race(const unsigned nthreads, const unsigned maxCount)
{
    std::cout << "We have " << nthreads << " threads in the race" << '\n';

    // All threads that we create below will increment the
    // following counter. Now, this counter is atomic.
    //
    // Note that only a small fraction of C++ types have atomic
    // counterparts. These are simple "trivially copyable" (technical
    // term) types, including bool, char, various integer types,
    // floating point numbers, etc.
    std::atomic<unsigned long> counter(0);

    // Compilers are allowed to implement atomic types using
    // mutexes... In a sense, this would defeat the purpose of
    // fast hardware-based atomic operations. Let's see if our
    // type is free of this problem.
    const bool lockFree = counter.is_lock_free();
    std::cout << "Our counter is " << (lockFree ? "" : "NOT ")
              << "lock-free. " << (lockFree ? "Great!" : "Duh...") << '\n';

    // Container for the threads
    std::vector<std::thread> threads;
    threads.reserve(nthreads);

    // Create the threads
    for (unsigned i=0; i<nthreads; ++i)
        threads.emplace_back(incrementCounter, &counter, maxCount);

    // Wait until all threads are finished
    for (auto& t : threads)
        t.join();

    // What would be the expected value of the counter
    // for the serial program?
    const unsigned long ex = (unsigned long)nthreads*maxCount;

    // Print the real and the expected values of the counter
    std::cout << "Counter is " <<  counter << ", expected " << ex << '\n';

    // We are done. Return value of 0 means success.
    return 0;
}

// The "main" function below is identical to the one in race.cc
int main(int argc, char *argv[])
{
    // Create the command line parser
    CmdLine cmdline(argc, argv);

    // Initialize variables which can be provided on the
    // command line to their default values
    unsigned nThreadsTotal = figureOutNumThreads();
    unsigned maxCount = 1000000;

    // Parse command line arguments
    try {
        cmdline.option("-m", "--maxCount") >> maxCount;
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
    return run_race(nThreadsTotal-1U, maxCount);
}
