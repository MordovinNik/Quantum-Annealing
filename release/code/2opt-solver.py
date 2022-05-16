
import numpy as np
import sys
import time
import itertools

def solve(M):
    n, _ = M.shape
    nodes = list(range(n))
    X = ring(nodes)
    best_matrix = X
    best_score = score(M, X)
    finish = False
    steps = 1
    while not finish:
        finish = True
        for pair in itertools.combinations(nodes, 2):
            copy = nodes.copy()
            i = pair[0]
            j = pair[1]
            copy[i], copy[j] = copy[j], copy[i]
            X = ring(copy)
            f = score(M, X)
            steps += 1
            if f < best_score:
                best_score = f
                best_matrix = X
                nodes = copy
                finish = False
                break
    return best_matrix, best_score, steps

in_file = sys.argv[1]
out_file = sys.argv[2]

M = np.loadtxt(in_file)
tic = time.perf_counter()
X, best_score, steps = solve(M)
toc = time.perf_counter()

def ring(nodes):
    n = len(nodes)
    A = np.zeros((n,n))
    for i in range(n):
        j = (i + 1) % n
        u = nodes[i]
        v = nodes[j]
        A[u,v] = A[v,u] = 1
    return A

def score(M, X):
    return np.sum(np.multiply(M, X))


with open(out_file, 'w') as f:
    f.write("Score: {0}\n".format(best_score))
    f.write("Solution:\n {0}\n".format(X))
    f.write("Steps: {0}\n".format(steps))
    f.write("Time: {0:0.4f} s\n".format(toc - tic))
