// This code illustrates thread synchronization with a thread barrier.
//
// TTU Computational Physics course (PHYS 4301/5322)
// I. Volobouev
// 02/04/2018

#include <thread>
#include <mutex>
#include <iostream>
#include <string>
#include <vector>

#include "ThreadBarrier.hh"


// This helper functor will be executed by the last thread at the
// barrier, while all other threads are still waiting for the barrier
// to open. Unless you run some extra threads, there will be no race
// conditions inside this code.
struct DimTheLights
{
    void operator()(const unsigned long cycle) const
    {
        if (cycle == 1U)
            std::cout << "The dinner was entertaining and delicious!\n";
        else if (cycle == 2U)
            std::cout << "The last person on the couch dims "
                      << "the lights and starts the movie player.\n";
    }
};


// Functor which will be run by each thread
class Person
{
public:
    // The constructor arguments are
    //   name           -- Object identifier.
    //   actionSequence -- A collection of "actions" to perform
    //                     (they will be simply printed to std::cout).
    //   barrier        -- A pointer to a thread synchronization barrier.
    //                     This class will not own this pointer.
    //
    // The "barrier" argument is allowed to be 0. This corresponds
    // to absence of synchronization.
    Person(const std::string& name,
           const std::vector<std::string>& actionSequence,
           AbsThreadBarrier* barrier)
        : name_(name), actions_(actionSequence), b_(barrier) {}

    // Method executed by the threads
    void operator()()
    {
        // Each person simply cycles over all assigned actions
        // in the order provided
        for (auto& action : actions_)
        {
            // Print the action performed at this moment.
            // To keep the output nice and tidy, we use
            // a mutex which protects std::cout from simultaneous
            // use by multiple threads. Note that, in order to
            // avoid deadlocks, we must release the lock before
            // any other synchronization can happen.
            {
                std::lock_guard<std::mutex> mutexGuard(printMutex_);
                std::cout << name_ << ' ' << action << ".\n";
            }

            if (b_)
            {
                // This is where the thread synchronization
                // actually happens. We wait at the barrier
                // until all other threads are done with the
                // current action.
                b_->wait();
            }
        }
    }

private:
    static std::mutex printMutex_;

    std::string name_;
    const std::vector<std::string>& actions_;
    AbsThreadBarrier* b_;
};

std::mutex Person::printMutex_;


int main()
{
    // The following variable can be used to turn thread
    // synchronization on (if "true") or off (if "false")
    const bool peopleAreFriends = true;

    // People in the party
    const std::vector<std::string> people{"Alex", "Jill", "John", "Mary"};

    // And this is what they are doing
    const std::vector<std::string> actionSequence{
        "sits at the table",
        "eats and talks",
        "moves to the couch",
        "watches the movie"
    };

    // Create a ThreadBarrier object for thread synchronization
    const unsigned nthreads = people.size();
    ThreadBarrier<DimTheLights> barrier{nthreads, true, DimTheLights()};

    // Do not synchronize threads if people are not friendly
    ThreadBarrier<DimTheLights>* bptr = peopleAreFriends ? &barrier : nullptr;

    // Container for the threads
    std::vector<std::thread> threads;
    threads.reserve(nthreads);

    // Create and run the threads, one per person
    for (auto& name : people)
        threads.emplace_back(Person(name, actionSequence, bptr));

    // Wait until all threads are finished
    for (auto& t : threads)
        t.join();

    std::cout << "These people are "
              << (peopleAreFriends ? "" : "NOT ") << "friends!\n";

    // We are done. Return value of 0 means success.
    return 0;
}
