"""
Created: Tue Jan 30 11:44:16 2018
Author: Ian Taulli
Description: creates a particular instance of qsolve
"""
import numpy as np
import qsolve as q

# the coefficents for (x-(10**10)*(x-(10**-10)
a = 1.0
b = -(10.0**20+1)/(10**10)
c = 1

ans1,ans2 = q.standard(a,b,c)
ans3,ans4 = q.modified(a,b,c)

print("results for standard: ",ans1," and ",ans2)
print("results for modified: ",ans3," and ",ans4)