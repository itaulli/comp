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

parray = np.array(P1, 'float')

size = 20
rfactor = 4.0
nx, ny = parray.shape
rmax = np.sqrt(nx**2+ny**2)

cluster = dla.Cluster(size)
gen = dla.CPP11Random()

for i in range(1,10):
    cluster.setCellValue(5+i, 5)
'''
while(cluster.getR() <= 0.5*size):
    phi0 = 2*np.pi*gen()
    radius0 = (rfactor/2.0)*(cluster.getR() + rmax)
    i0 = int(size + radius0*np.sin(phi0))
    j0 = int(size + radius0*np.cos(phi0))

    walker = dla.Walker(parray)
    walker.setPos(i0, j0)

    sim = dla.Simulation(rfactor, gen)
    if(sim.walk(walker, cluster)): print(cluster.getR())
'''

result = cluster.convert()

fig = plt.figure()
ax = fig.add_subplot(111)
mshow = ax.matshow(result)
ax.set_xlabel('column number')
ax.set_ylabel('row number')
fig.colorbar(mshow, aspect=10)
plt.savefig('test.pdf')
plt.close()
