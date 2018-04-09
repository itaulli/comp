"""
Created: Tue Jan 30 11:44:16 2018
Author: Ian Taulli
Description: creates a particular instance of qsolve
"""
import numpy as np
import qsolve as q

# the coefficents for (x+200)*(x+1/200)
a = 1
b = 200
c = 1

ans1,ans2 = q.standard(a,b,c)
ans3,ans4 = q.modified(a,b,c)
truth = 3.0*np.sqrt(1111) - 100

print("solves the equation x^2 + 200*x + 1 = 0")
print("results for standard: {:.20f} and {:.20f}".format(ans1,ans2))
print("results for modified: {:.20f} and {:.20f}".format(ans3,ans4))
print("notice the difference between the second solutions in the 14th decimal place")
print("the true solution is closer to 3*sqrt(1111) - 100 = {:.20f}".format(truth))
print("the additional error in the standard solution can be attributed to subtractive cancellation")
print("this is an example of the general case where b^2 >> 4ac")
print("so that sqrt(b^2-4ac) ~ b, forcing a larger error after subtraction")