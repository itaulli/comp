"""
Created: Thu Jan 25 11:27:50 2018
Author: Ian Taulli
Description:
"""
import matplotlib.pyplot as plt

def plot(x):

    temp = []
    number = []
    xlist = []
    ylist = []
    file = open(x)

    for line in file:
    
        if line.startswith(('#',' ')):
            continue
    
        table = str.maketrans(',',' ')
        line = line.translate(table)
    
        x = line.split(maxsplit=1)
        temp += x

    for entry in temp:

        entry = entry.strip('\n')
        entry = float(entry)
        number.append(entry)

    xlist = number[0::2]
    ylist = number[1::2]

    plt.plot(xlist,ylist)
    ax = plt.gca()
    ax.set_title('fig. 1 (Taulli)')
    plt.savefig('fig1.pdf')