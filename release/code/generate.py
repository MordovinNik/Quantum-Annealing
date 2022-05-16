import random
import numpy as np
import sys

n = int(sys.argv[1])
file = sys.argv[2]
M = np.zeros((n,n))
for i in range(0, n):
    for j in range(0, n):
        if i != j:
            M[i, j] = random.randint(1, n)   

np.savetxt(file, M, fmt='%d')
