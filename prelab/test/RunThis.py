"""
Created: Wed Jan 24 13:49:50 2018
Author: Ian Taulli
Description: takes the data from xy.txt and makes a plot
"""
import matplotlib.pyplot as plt

#initailize some lists and open the file
temp = []
number = []
xlist = []
ylist = []
file = open('xy.txt')

for line in file:
    
    #skip lines that are comments or empty space
    if line.startswith(('#',' ')):
        continue
    
    #turn all the commas into spaces
    table = str.maketrans(',',' ')
    line = line.translate(table)
    
    #split the x and y values and stack them
    x = line.split(maxsplit=1)
    temp += x

for entry in temp:
    
    #turn each entry into a float object
    entry = entry.strip('\n')
    entry = float(entry)
    number.append(entry)

#split the x and y values into two lists
xlist = number[0::2]
ylist = number[1::2]

#plot the lists
plt.plot(xlist,ylist)
ax = plt.gca()
ax.set_title('HW1 (Taulli)')
plt.savefig('fig1.pdf')