#ifndef ABSTHREADBARRIER_HH_
#define ABSTHREADBARRIER_HH_

// Base class which defines the thread barrier interface for its users
struct AbsThreadBarrier
{
    // We need a virtual destructor for proper inheritance
    inline virtual ~AbsThreadBarrier() {}

    // Threads will wait at the barrier by calling this function.
    // It is pure virtual, so it must be implemented by derived classes.
    virtual void wait() = 0;
};

#endif // ABSTHREADBARRIER_HH_
