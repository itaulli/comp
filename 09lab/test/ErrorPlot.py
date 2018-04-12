import numpy as np
import matplotlib.pyplot as plt

xvals = np.linspace(0, 1.2, 100)
yvals = abs(1-xvals-xvals**2)
line = np.ones(len(xvals))

plt.figure()
plt.plot(xvals, yvals, 'b')
plt.plot(xvals, line, 'r--')
plt.title('Error Amplification')
plt.xlabel('discreatization factor')
plt.ylabel('magnitude ksi')
plt.savefig('ErrorPlot.pdf')
plt.close()
