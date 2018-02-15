"""
This module generates Niederreiter's quasi-random numbers. Based on the TOMS
algorithm 823, "Implementing Scrambled Digital Sequences", by H. S. Hong
and F. J. Hickernell.

To use this module, call the "init()" function first, and then call
the next() function whenever you need the next quasi-random vector.

The arguments of the init(d, nskip, scrambling) functions are:

d:     The dimensionality of the space, 2 <= d <= 40. This is a required
       argument.
       
nskip: The number of vectors to skip at the beginning of the sequence.
       It is sometimes useful to let the generator to "warm up" before
       using the vectors. If you are going to use N vectors, it is common
       to skip 2**M vectors at the beginning, where M is the smallest
       integer for which 2**M >= N. Default value of this argument is 0.

scrambling: Type of the additional scrambling of the quasi-random digits.
       0 -- No Scrambling (this is the default)
       1 -- Owen type Scrambling
       2 -- Faure-Tezuka type Scrambling
       3 -- Owen + Faure-Tezuka type Scrambling
"""

__author__="Igor Volobouev (i.volobouev@ttu.edu)"
__version__="0.3"
__date__ ="Feb 11 2016"

import quasi_random

__dimensionality = 0

def init(dimensionality, nskip=0, scrambling=0):
    if dimensionality < 2 or dimensionality > 40:
        raise ValueError("Sequence dimensionality is out of range")
    if nskip < 0:
        nskip = 0
    if scrambling < 0 or scrambling > 3:
        raise ValueError("Invalid scrambling")
    quasi_random.sinlo2(dimensionality, nskip, scrambling)
    quasi_random.sgolo2()
    global __dimensionality
    __dimensionality = dimensionality

def next():
    global __dimensionality
    return quasi_random.sgolo2()[0:__dimensionality]
