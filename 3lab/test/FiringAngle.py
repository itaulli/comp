"""
Created: Wed Feb 14 11:44:53 2018
Author: Ian Taulli
Description: given some firing angle and initial parameters, returns the maximum range
"""
from cpode import *
from cpforces import *
import math
import numpy as np
from v3 import *
import matplotlib.pyplot as plt
from scipy import optimize as so

def max_range(theta):
    
    #mass of the projectile (kg)
    m = 4e-3
    #initial velocity (m/s)
    speed = 930
    #initial hieght (m)
    h0 = 1.0
    #cross-sectional area (m^2)
    area = 2.45e-5
    #air density (kg/m^3)
    density = 1.2
    
    #initialize the force classes
    Fg = ForceOfGravity(m)
    Fd = BulletDrag(area, density)
    
    #get the ODE solver
    bullet = RK4(Fg + Fd, m)
    
    #initial conditions
    x0 = V3(0.0, h0, 0.0)
    v0 = V3(speed*math.cos(theta), speed*math.sin(theta), 0.0)
    dt = 1e-3
    
    #run the solver and get the coordinates
    bullet.run(x0, v0, dt, AboveGround())
    xcoords = np.array([vector.x for vector in bullet.x])
    ycoords = np.array([vector.y for vector in bullet.x])
    
    #shift the last 4 coordinates for the polynomial fit
    xshift = xcoords[-4:]-xcoords[-1]
    yshift = ycoords[-4:]
    
    #fit to a third degree polynomial y = a + b*x + c*x^2 + d*x^3
    coef = np.polynomial.polynomial.polyfit(xshift,yshift,3)
    
    #find the right root and shift it back
    roots = np.polynomial.polynomial.polyroots(coef)
    xmax = roots[2]+xcoords[-1]
    
    return abs(xmax)

#makes a plot with some trajectories
'''
angles = np.arange(0.1, 0.9, 0.1)
for angle in angles:
    xcoords, ycoords = max_range(angle)
    plt.plot(xcoords, ycoords, label=angle)
ax = plt.gca()
ax.grid(True)
ax.set_title('Example Trajectories')
ax.set_xlabel('x values')
ax.set_ylabel('height')
ax.legend(title='angle')
plt.savefig('test.pdf')
plt.close()
'''
#prints a list of angles and their ranges
'''
angles = np.arange(0.4,0.65,0.01)
ranges = np.zeros(len(angles))
for i in range(len(angles)):
    ranges[i] = max_range(angles[i])
    print('angle = {:.2f}, range = {:.1f}'.format(angles[i],ranges[i]))
'''
#calculation for the average relative precision
'''
angles = np.arange(0.5, 0.6, 0.01)
range_vals = np.zeros(len(angles))
rel_prec = np.zeros(len(angles))
for i, angle in enumerate(angles):
    range_vals[i] = max_range(angle)
for i in np.arange(1,len(angles)):
    range_diff = abs(range_vals[i]-range_vals[i-1])
    rel_prec[i] = range_diff/range_vals[i]
avg_prec = np.sum(rel_prec)/len(rel_prec)
print(avg_prec)
'''
#plotting stuff
'''
plt.plot(angles, range_vals/1000, linewidth=0.5)
ax = plt.gca()
ax.grid(True)
ax.set_title('Estimation of Relative Precision')
ax.set_xlabel('firing angle')
ax.set_ylabel('maximum range')
plt.savefig('test.pdf')
plt.close()
'''
#Brent's method optimization

def invert(x):
    return -1.0*max_range(x)
bracket = (0.5,0.6)
angle = so.brent(invert, brack=bracket, tol=0.06)
frac = float(np.pi/angle)
deg = angle*180/np.pi
print('theta = pi/{:.3f} or {:.2f} degrees'.format(frac, deg))

