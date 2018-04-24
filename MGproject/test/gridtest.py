import numpy as np
from MGtools import *

a = np.ones((1000,1000))
b = np.ones(a.shape)

limit = int(0.8*np.log2(a.shape[0]))

for i in range(limit):
    print(a.shape)
    a = restrict(a)

print('SWITCH')

for i in range(limit):
    a = interpolate(a)
    print(a.shape)
