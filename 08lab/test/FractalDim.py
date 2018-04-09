import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

for i in range(1,6):
    for j in range(1,4):
        file_dir = '/Users/ian/work/comp/8lab/test/arrays/DimArrays_type{:d}_{:d}.npz'.format(j,i)
        load_file = np.load(file_dir)
        xvals = load_file['x']
        yvals = load_file['y']

        logx = np.log(xvals)
        logy = np.log(yvals)

        slope, intercept, r_value, p_value, std_err = stats.linregress(logx, logy)

        plt.figure()
        plt.loglog(xvals, yvals, label='slope = {:.4f}'.format(slope))
        ax = plt.gca()
        ax.grid()
        ax.set_title('Fractal_type{:d}_{:d}'.format(j,i))
        ax.set_xlabel('log(radius)')
        ax.set_ylabel('log(rho)')
        ax.legend()
        plt.savefig('type{:d}_{:d}_dim.pdf'.format(j,i))
        plt.close()
