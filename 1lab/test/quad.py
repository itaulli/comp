"""
Created: Tue Jan 30 11:44:16 2018
Author: Ian Taulli
Description: creates a particular instance of qsolve
"""
import numpy as np
import qsolve as q

# the coefficents
a = 1
b = -10.0**20
c = 1

#calls the solution functions
ans1,ans2 = q.standard(a,b,c)
ans3,ans4 = q.modified(a,b,c)

#creates the output
print('standard quadriatic formula: {:.2f} and {:.2f}'.format(ans1,ans2))
print('modified algorithm: {:.2f} and {:.2f}'.format(ans3,ans4))