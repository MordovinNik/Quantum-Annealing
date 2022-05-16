import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Qt5Agg")
file = '../data/n8/solutions/brute-force/scores1.txt'
M = np.loadtxt(file)
fig, ax = plt.subplots()
ax.plot(M[:,0], M[:,1])
ax.set_xlabel('combinations', fontsize=16)
ax.set_ylabel(r'$\sum M .* X$', fontsize=16)
fig.show()
input("Press ENTER to exit")
