"""
Created: Wed Jan 24 13:49:50 2018
Author: Ian Taulli
Description: takes the data from xy.txt and makes a plot
"""

import matplotlib.pyplot as plt

temp = []
xlist = []
ylist = []
file = open('xy.txt')

for line in file:
    
    if line.startswith(('#',' ')):
        continue
    
    table = str.maketrans(',',' ')
    line = line.translate(table)
    
    x = line.split(maxsplit=1)
    temp += x

for i in range(len(temp)):
    
    entry = temp[i]
    entry = entry.strip('\n')
    number = float(entry)
    
    if i%2 == 0:
        xlist += [number]
    
    if i%2 == 1:
        ylist += [number]

plt.plot(xlist,ylist)
ax = plt.gca()
ax.set_title('fig. 1 (Taulli)')
plt.savefig('fig1.pdf')