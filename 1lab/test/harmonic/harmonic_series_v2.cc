//
// I will assume that you already understand the basics of the C++
// program structure and include files. Therefore, the comments in this
// file are not going to cover the concepts explained previously in
//
// http://www.phys.ttu.edu/~igvol/ComputationalPhysics/Tutorials/Tutorial3/hello_explained.cc
//
#include <iostream>

int main()
{
    // The following statement is known as "variable declaration".
    // It tells the compiler that we are going to employ an unsigned
    // integer variable named "k" inside this function. On archer, this
    // is a 32-bit integer which can take values between 0 and 2^32 - 1.
    // Upon encountering this statement, the compiler will reserve an
    // appropriate amount of memory (four bytes) to hold this variable.
    // Complete C++ statements must be terminated by a semicolon (;).
    // It is usually best to write just one complete statement per line.
    // This improves code readability.
    //
    unsigned k;

    // Note that after the previous statement the value of "k" remains
    // undefined. There are only two meaningful actions that you can perform
    // with such a variable: to assign a value to it and to take its address.
    // It would be a mistake to use it in any other way (for example,
    // as an argument of an opertator or a function). Moreover, the compiler
    // is not guaranteed to detect such a mistake, especially if you work
    // with the variable address rather than with the variable itself.
    // Because of this it is usually safer both to declare a variable and
    // to initialize it at the same time, as illustrated by the next statement.
    //
    // The following statement declares variables "sum" and "old_sum"
    // and assigns initial values to them (this is known as "variable
    // initialization"). "float" is a 32-bit floating point number. ".f"
    // after the number indicates a 32-bit floating point constant.
    //
    float sum = 0.f, old_sum = -1.f;

    // The C++ "for" statement performs looping. It looks like this:
    //
    // for (A; B; C)
    // {
    //     D;
    //     E;
    //     ...
    // }
    //
    // The collection of statements inside the curly brackets is known as the
    // "loop body". The statement A (which is optional and can be omitted)
    // is executed once before everything else. Then the statement B whose
    // result type must be boolean or convertible to boolean is executed
    // (the statement B is known as the "loop condition"). If the result of B
    // evaluation is "false" then nothing else happens. If the result of
    // B evaluation is "true" then the loop body is executed, followed by
    // the optional statement C. After this, the sequence (B, loop body, C)
    // continues until the loop condition B returns "false".
    //
    // The idiomatic way of repeating something exactly n times (with n known
    // beforehand) looks like this:
    //
    // const unsigned long n = (some number that you have calculated);
    //
    // for (unsigned long i = 0; i < n; ++i)
    // {
    //      ... do something inside the loop body ...
    // }
    //
    // It is also possible to terminate the loop execution from inside the
    // loop body by using the "break" statement. This is sometimes useful
    // if the termination condition has to rely on variables declared inside
    // the loop body or if execution of statement C is not desirable after
    // the last loop cycle.
    //
    // The loop condition can be omitted as well in which case the "for"
    // statement works as if the condition always returns "true". For example,
    // the idiomatic C++ infinite cycle looks as follows:
    //
    // for (;;)
    // {
    //      ... do something inside the loop body ...
    //      ... you will likely need a "break" statement somewhere ...
    // }
    //
    // Note that, even if some or all of A, B, and C statements are omitted,
    // there must always be exactly two semicolons inside parentheses following
    // the "for" keyword.
    //
    // In the "for" statement used below, A, B, and C are as follows:
    //
    // A:  k = 1
    // B:  old_sum != sum
    // C:  ++k
    //
    // Statement A assigns the value of 1 to the variable k (which was
    // undefined before this). In this context, "=" serves as the
    // "assignment operator".
    //
    // Statement B uses operator "not equal": !=. This operator
    // returns "true" in case values of "old_sum" and "sum" are
    // distinct.
    //
    // Statement C increments the value of k by one.
    //
    for (k = 1; old_sum != sum; ++k)
    {
        // The following statement uses the assignment operator "=".
        // The value of "sum" is assigned to the variable "old_sum".
        // "sum" itself is not modified.
        //
        old_sum = sum;

        // The following statement is somewhat complicated.
        //
        // Operator "+=" in known as the "in-place addition". The statement
        // a += b is a shorthand notation for a = a + b. The operator +=
        // is executed last, after the right hand side is evaluated (the
        // C++ operator precedence rules can be looked up, for example,
        // at http://www.cplusplus.com/doc/tutorial/operators/ )
        //
        // The "static_cast<float>(1)" operation (static cast) is executed
        // first. Here, it converts an integer constant into a 32-bit floating
        // point value. The subsequent division implicitly converts the
        // unsigned integer k into a 32-bit floating point value before the
        // division is performed. This is a general rule for simple numeric
        // types: binary mathematical operations (multiplication, division,
        // addition, subtraction) always act on objects of the same type
        // and produce the result of the same type. If the types of the
        // operator arguments are not the same, one argument will be converted
        // into the type of the other before the operation. The conversion is
        // performed towards the numeric type that has larger range. Thus
        // integers are converted into floats and not the other way around.
        //
        // BTW, according to this rule (the type of the result is the same
        // as the type of the arguments) the value of 1/k without the cast
        // is 0 for all k > 1. This is because the result has to be integer,
        // so its fractional part is simply truncated.
        //
        // As you can easily figure out by inspecting the loop condition
        // statement, the cycle will be terminated as soon as the in-place
        // addition does not change the sum (that is, series "converge").
        //
        sum += static_cast<float>(1)/k;
    }

    // Print out the value of k upon the loop termination
    // and the calculated sum
    //
    std::cout << "k is " << k << ", sum is " << sum << '\n';

    // We are done. Return value of 0 means success.
    return 0;
}
