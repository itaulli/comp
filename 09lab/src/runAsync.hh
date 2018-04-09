#ifndef RUNASYNC_HH_
#define RUNASYNC_HH_

// The "runAsync" function is a wrapper around std::async. It fixes
// the problem with the default behavior of asynchronous tasks.
// By default, the decision run now/run later can be made by the
// C++ runtime library which results in potentially indeterministic
// behavior and Heisenbugs, especially if thread_local variables are
// used. Here, we are forcing each task to run immediately in a new thread.

#include <future>

template <typename F, typename... Ts>
inline auto runAsync(F&& f, Ts&&... params) {
    return std::async(std::launch::async, std::forward<F>(f),
                      std::forward<Ts>(params)...);
}

#endif // RUNASYNC_HH_
