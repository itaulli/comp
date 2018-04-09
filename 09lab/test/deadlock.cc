// This code illustrates a deadlock condition in multithreaded code.
//
// TTU Computational Physics course (PHYS 4301/5322)
// I. Volobouev
// 02/04/2018

#include <thread>
#include <mutex>
#include <iostream>
#include <cassert>
#include <utility>

#include "CmdLine.hh"

// Function to increment and print the counters
static void workWithCounters(const unsigned threadNumber,
                             unsigned long* cnt1, std::mutex* m1,
                             unsigned long* cnt2, std::mutex* m2,
                             const unsigned maxCount)
{
    // Assert all arguments passed by pointer. We don't
    // expect that any of these pointers can be null.
    assert(cnt1);
    assert(m1);
    assert(cnt2);
    assert(m2);

    // Increment and print the counters, protecting access
    // to each counter with its corresponding mutex
    for (unsigned i=0; i<maxCount; ++i)
    {
        // Increment the fisrt counter, avoiding the race
        // condition with a mutex. "++*cnt1" is guaranteed
        // not to throw an exception, so we don't need
        // a lock guard here.
        {
            m1->lock();
            ++*cnt1;
            m1->unlock();
        }

        // Increment the second counter in a similar manner
        {
            m2->lock();
            ++*cnt2;
            m2->unlock();
        }

        // Print the counters. This operation involves both
        // counters, so we acquire both locks.
        {
            std::lock_guard<std::mutex> guard1(*m1);
            std::lock_guard<std::mutex> guard2(*m2);
            std::cout << "Thread " << threadNumber << ": cnt1 = "
                      << *cnt1 << ", cnt2 = " << *cnt2 << '\n';
        }
    }
}

int main()
{
    const unsigned maxCount = 1000000;

    // Suppose that we have two counters to work with and two mutexes
    // to protect them
    unsigned long cnt1 = 0, cnt2 = 0;
    std::mutex m1, m2;

    // Create the threads which will work with the counters. Note the
    // swapped order of counters and mutexes in the second thread w.r.t.
    // the first. While this example is somewhat contrived, in reality
    // you might encounter situations in which this order is out of your
    // control (e.g., working with database records in user searches).
    std::thread t1{workWithCounters, 1, &cnt1, &m1, &cnt2, &m2, maxCount};
    std::thread t2{workWithCounters, 2, &cnt2, &m2, &cnt1, &m1, maxCount};

    // Wait until the threads are finished
    t1.join();
    t2.join();

    // We are done. Return value of 0 means success.
    return 0;
}
