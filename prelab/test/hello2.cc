// Header files for standard library classes used in this program
#include <vector>
#include <string>
#include <iostream>

// Header file for "CmdLine" command line parser
#include "CmdLine.hh"

// "main" with standard arguments
int main(int argc, char *argv[])
{
    // Create an instance of CmdLine
    CmdLine cmdline(argc, argv);

    // Program parameters whose values you want to modify using
    // command line arguments, initialized to some default values
    int i = 0;
    double d = 0;
    bool b = false;
    std::string requiredOption;
    std::vector<std::string> positionalArgs;

    // Parsing of the command line options is performed inside
    // the following "try" block. In case something goes wrong,
    // the exception of type "CmdLineError" is thrown.
    try {
        // Arguments of the "option" method of CmdLine class are short
        // and long versions of the option name. Long version can be
        // omitted. If you want to use the long version only, call the
        // two-argument method with the short version set to 0.
        cmdline.option("-i", "--integer") >> i;
        cmdline.option("-d") >> d;

        // Options that must be present on the command line. Use the
        // "require" method of the CmdLine class to process such options.
        // If a required option is not found, an exception is thrown.
        cmdline.require("-r", "--required") >> requiredOption;

        // Switches that do not require subsequent arguments
        b = cmdline.has("-b", "--booleanSwitch");

        // Declare the end of option processing. Unconsumed options
        // will cause an exception to be thrown.
        cmdline.optend();

        // Process all remaining arguments. This example illustrates
        // the case in which you want to use a variable number of such
        // arguments (this could be, for example, a list of files).
        // If, instead, the number of such arguments is known and fixed,
        // a more efficient way to process them would proceed along the
        // following lines:
        //
        // if (cmdline.argc() != n_expected)
        //     throw CmdLineError("wrong number of command line arguments");
        // cmdline >> arg0 >> arg1 >> ...;
        //
        while (cmdline)
        {
            std::string s;
            cmdline >> s;
            positionalArgs.push_back(s);
        }
    }
    catch (const CmdLineError& e) {
        // Print the error message and exit with a non-zero status.
        // The "progname" method of the CmdLine class returns the
        // name of the executable.
        std::cerr << "Error in " << cmdline.progname() << ": "
                  << e.str() << std::endl;
        return 1;
    }

    // Print out the options. Of course, in more realistic scenarios
    // you are probably going to call some functions here which perform
    // some useful work.
    std::cout << "i = " << i << '\n'
              << "d = " << d << '\n'
              << "b = " << std::boolalpha << b << '\n'
              << "requiredOption is \"" << requiredOption << "\"\n";

    // Print out the positional arguments
    std::cout << "Simple arguments are: ";
    const std::size_t nArgs = positionalArgs.size();
    for (std::size_t i = 0; i < nArgs; ++i)
    {
        if (i)
            std::cout << ", ";
        std::cout << '"' << positionalArgs[i] << '"';
    }
    std::cout << std::endl;

    // We are done
    return 0;
}    
