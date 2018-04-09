// This code illustrates a race condition in multithreaded programming.
//
// TTU Computational Physics course (PHYS 4301/5322)
// I. Volobouev
// 02/04/2018

#include <thread>
#include <iostream>
#include <vector>
#include <cassert>
#include <mutex>
#include "figureOutNumThreads.hh"
#include "CmdLine.hh"

// Function to increment a counter. This function
// will be run simultaneously by several threads.


std::mutex obj_mutex;

static void incrementCounter(unsigned long* counter, const unsigned maxCount)
{
    // Assert all arguments passed by pointer
    assert(counter);
    obj_mutex.lock();
    for (unsigned i=0; i<maxCount; ++i)
        {++*counter;}
    obj_mutex.unlock();
}

static int run_race(const unsigned nthreads, const unsigned maxCount)
{
    std::cout << "We have " << nthreads << " threads in the race" << '\n';

    // All threads that we create below will increment the
    // following counter
    unsigned long counter = 0;

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
