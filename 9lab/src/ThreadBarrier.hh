#ifndef THREADBARRIER_HH_
#define THREADBARRIER_HH_

#include <atomic>
#include <cassert>

#include "AbsThreadBarrier.hh"

// A helper class
struct DummyCallback
{
    inline void operator()(unsigned long) const {}
};

//
// The ThreadBarrier class implements the barrier thread synchronization
// method. Imagine that you have a group of threads working together on
// some task. A barrier allows for faster moving threads to wait until
// all other threads in the group reach the same point. It is expected
// that each thread in the group will hold a reference to the same
// ThreadBarrier object and that all threads will call the "wait()"
// member function for synchronization.
//
// This particular barrier implementation relies on C++ atomic types.
// These types guarantee that certain operations (called atomic operations)
// are free from the race condition and that the values of atomic variables
// look the same to all threads (at least in the sequentially consistent
// memory model used by default). The main cost of using atomic variables
// is known as the "cache ping-pong": whenever some thread modifies such
// variables, this change has to propagate to the cache of all other CPU
// cores before these cores can resume their calculations. If the system
// has multiple CPUs (rather than just multiple cores on a single CPU),
// this propagation has to proceed through the memory hardware and can be
// quite costly, as all other CPUs working on this task have to stop
// their calculations and wait.
//
// ThreadBarrier is a "class template" because proper operation of
// this class does not depend on the exact type of "lastThreadAction"
// constructor argument. Consider the following example: the code which
// calculates the sum of an array of doubles and the code which calculates
// the sum of an array of integers are likely to look identical in all
// respects apart from the type of the summands. The C++ facility which
// allows us to use the same summation code in both situations and, at
// the same time, still perform type checking during the compilation stage
// is called "templates". For more details, see
// http://www.cplusplus.com/doc/oldtutorial/templates/
//
template<class Functor = DummyCallback>
class ThreadBarrier : public AbsThreadBarrier
{
public:
    // The constructor arguments are as follows:
    //
    //  nThreads         -- Number of threads that will be working with
    //                      this barrier. Must be positive.
    //
    //  lastThreadAction -- An arbitrary functor (callback) which will be
    //                      executed by the last thread arriving at the
    //                      barrier before the barrier opens. The argument
    //                      of the call will be the barrier count. Note that
    //                      this functor is passed by value so its copying
    //                      should not demand a lot of resources. If you
    //                      don't need a callback then don't provide this
    //                      argument. Note that in this case you still
    //                      need to use the angle brackets to declare the
    //                      barrier type in your code: "ThreadBarrier<>".
    //
    //  yieldWhenWaiting -- This argument specifies whether a thread
    //                      waiting at the barrier should yield to other
    //                      threads. See comments inside the body of the
    //                      code for further explanations.
    //
    // Note that the actual number of threads working simultaneously with
    // this barrier (i.e., calling the "wait" function) should not exceed
    // the "nThreads" constructor argument. It is the responsibility of
    // the user of this class to ensure that this is, indeed, the case.
    // Otherwise the barrier is not going to function as intended. 
    //
    inline ThreadBarrier(const unsigned nThreads, const bool yieldWhenWaiting,
                         const Functor lastThreadAction = DummyCallback())
        : nThreads_(nThreads),
          nRunning_(nThreads),
          count_(0),
          lastThreadAction_(lastThreadAction),
          yield_(yieldWhenWaiting)
    {
        // Make sure that the "nThreads" argument is positive.
        // Otherwise the barrier logic will not work.
        assert(nThreads);
    }

    inline virtual ~ThreadBarrier() {}

    inline virtual void wait() override
    {
        // Each thread gets its own copy of "myCount" variable
        const unsigned long myCount = count_;

        // "--nRunning_" is an atomic operation, guaranteed to
        // be executed by one thread at a time
        if (--nRunning_)
        {
            // This is not the last thread arriving at the barrier.
            // Enter the wait cycle. Wait until the value of "count"
            // changes (it will be incremented by the last thread
            // arriving at the barrier).
            while (count_ == myCount)
                if (yield_)
                    // Yield to other threads. The operating system will
                    // move this thread to the end of the thread queue.
                    // Note that the operation of "yielding" itself takes
                    // some CPU cycles, so it is not obvious apriori
                    // whether it is beneficial to yield (likely not if all
                    // threads reach the barrier at approximately the same
                    // time). This is why we yield conditionally on the
                    // "yield_" variable whose optimal value could be
                    // different for differnt algorithms and running
                    // conditions.
                    std::this_thread::yield();
        }
        else
        {
            // This is the last thread arriving at the barrier.
            // Perform the requested action.
            lastThreadAction_(myCount);

            // Prepare the next barrier cycle
            nRunning_ = nThreads_;

            // Open the barrier
            ++count_;
        }
    }

private:
    // Number of threads that need to reach the barrier
    // in every cycle before the barrier opens
    const unsigned nThreads_;

    // Number of threads that still needs to arrive at
    // the barrier for the barrier to open in the current
    // open/close cycle
    std::atomic<unsigned> nRunning_;

    // The number of times the barrier has been reached by all
    // threads (and opened). It is atomic because all threads
    // need to see the same "count_" value.
    std::atomic<unsigned long> count_;

    // An action that should performed by the last thread
    // reaching the barrier, just before the barrier becomes
    // open again
    Functor lastThreadAction_;

    // This variable will tell the class whether a thread
    // waiting at the barrier should yield to other threads
    const bool yield_;
};

#endif // THREADBARRIER_HH_
