#include <thread>
#include <algorithm>

#include "figureOutNumThreads.hh"

unsigned figureOutNumThreads()
{
    // Determine the maximum number of concurrent threads
    // supported by this computer. For Intel CPUs with
    // hyper-threading we expect to get twice the number
    // of cores.
    const unsigned maxThreads = std::thread::hardware_concurrency();

    // We will grab some reasonable fraction of CPU resources.
    // Of course, if you work on your own computer, you might
    // want to grab a larger fraction. Note, however, that the
    // operating system will still run multiple other processes
    // simultaneously with your program, so it is usually not
    // a good idea to assume that you can effectively employ
    // all "maxThreads" threads.
    //
    // This argument notwithstanding, we will usually need to run
    // at least two threads in addition to the main thread in
    // order to illustrate concurrency. Note that the "std::max"
    // function is declared in the standard header <algorithm>.
    //
    return std::max(maxThreads/2U+1U, 3U);
}
