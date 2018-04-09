import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import dla

P1 = ((0.7071, 1.0, 0.7071),
      (1.0, 0.0, 1.0),
      (0.7071, 1.0, 0.7071))

P2 = ((0.5657, 1.0, 0.7071),
      (0.8, 0.0, 1.0),
      (0.5657, 1.0, 0.7071))

P3 = ((0.7071, 0.0, 1.0, 0.0,  0.7071),
      (1.0, 0.0, 0.0, 0.0, 1.0),
      (0.7071, 0.0, 1.0, 0.0, 0.7071))

parray = np.array(P3, 'float')

size = 600
rfactor = 4.0
nx, ny = parray.shape
rmax = np.sqrt(nx**2+ny**2)

cluster = dla.Cluster(size)
gen = dla.CPP11Random()

counter = 0
while(cluster.getR() < 0.5*size - 4):
    phi0 = 2*np.pi*gen()
    radius0 = (rfactor/2.0)*(cluster.getR() + rmax)
    i0 = int(size/2 + radius0*np.sin(phi0))
    j0 = int(size/2 + radius0*np.cos(phi0))
    walker = dla.Walker(parray)
    walker.setPos(i0, j0)
    
    sim = dla.Simulation(rfactor, gen)
    sim.walk(walker, cluster)


result = cluster.convert()

x_array = np.linspace(0.1*cluster.getR(), 0.6*cluster.getR(), 20)
y_array = np.zeros(len(x_array))
for k, radius in enumerate(x_array):
    counter = 0
    for i in range(size):
        for j in range(size):
            if(cluster.dist(i,j) < radius):
                if(cluster.isFilled(i,j)):
                    counter += 1
    y_array[k] = counter

np.savez('DimArrays_type3_5'.format(size), x=x_array, y=y_array)

fig = plt.figure()
ax = fig.add_subplot(111)
mshow = ax.matshow(result)
ax.set_xlabel('column number')
ax.set_ylabel('row number')
fig.colorbar(mshow, aspect=10)
plt.savefig('FactalPlot_type3_5.pdf'.format(size))
plt.close()
