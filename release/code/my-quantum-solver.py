import numpy as np
import sys
from dwave.embedding.chain_strength import scaled
from dwave.system.composites import EmbeddingComposite
from dwave.system.samplers import DWaveSampler
import dwave.inspector
import time

def index(i, j, n):
    if i == j:
        raise ValueError
    elif i > j:
        return index(j, i, n)
    else:
        return int(i*n - i*(i+1)/2 + j - (i+1))

def build_constraint_matrix(n):
    m = int(n*(n-1)/2)
    C = np.zeros((m,m))
    for i in range(0, n):

        for j in range(0, n):
            if i == j:
                continue
            k = index(i, j, n)
            C[k,k] += -3

        for a in range(0, n):
            for b in range(0, n):
                if a == b or a == i or b == i:
                    continue
                ia = index(i,a,n)
                ib = index(i,b,n)
                C[ia,ib] += 1
    return C

def build_objective_matrix(M):
    n, _ = M.shape
    m = int(n*(n-1)/2)
    Q = np.zeros((m,m))
    k = 0
    for i in range(0, n):
        for j in range(i+1, n):
            Q[k, k] = (M[i,j] + M[j,i])
            k += 1

    return Q

def is_valid_solution(X):
    rows, cols = X.shape
    for i in range(rows):
        count = 0
        for j in range(cols):
            if X[i,j] == 1:
                count += 1
        if not count == 2:
            return False
    return True
    
def build_solution(sample):
    n, _ = M.shape
    m = len(sample)
    assert m == int(n*(n-1)/2)
    X = np.zeros((n,n))
    k = 0
    for i in range(n):
        for j in range(i+1, n):
            X[i,j] = X[j,i] = sample[k]
            k += 1
    return X

def score(M, X):
    return np.sum(np.multiply(M, X))    

in_file = sys.argv[1]
out_file = sys.argv[2]
num_samples = 100

M = np.loadtxt(in_file)
Q = build_objective_matrix(M)
lagrange_multiplier = np.max(np.abs(M))


n, _ = M.shape
C = build_constraint_matrix(n)

qubo = Q + lagrange_multiplier * C
sampler = EmbeddingComposite(DWaveSampler())
t0 = time.perf_counter()
sampleset = sampler.sample_qubo(qubo, num_reads=num_samples, chain_strength=scaled)
t1 = time.perf_counter()
dwave.inspector.show(sampleset)
have_solution = False
problem_id = sampleset.info['problem_id']
chain_strength = sampleset.info['embedding_context']['chain_strength']
with open(out_file, 'w') as f:
    f.write(f"Problem Id: {problem_id}\n")
    count = 0
    for e in sampleset.data(sorted_by='energy'):
        sample = e.sample
        energy = e.energy
        num_occurrences = e.num_occurrences
        chain_break_fraction = e.chain_break_fraction
        X = build_solution(sample)
        if is_valid_solution(X):
            have_solution = True
            score = score(M, X)
            f.write(f"Solution:\n")
            f.write(f"{X}\n")
            f.write(f"Score: {score}\n")
            f.write(f"{sample}\n")
            f.write(f"index: {count}\n")
            f.write(f"energy: {energy}\n")
            f.write(f"num_occurrences: {num_occurrences}\n")            
            f.write(f"chain break fraction: {chain_break_fraction}\n")            
            break
        count += 1
    f.write(f"chain strength: {chain_strength}\n")
    f.write(f"lagrange multiplier: {lagrange_multiplier}\n")
    f.write(f"Time: {t1-t0:0.4f} s\n")
    if not have_solution:
        chain_break_fraction = np.sum(sampleset.record.chain_break_fraction)/num_samples
        f.write("did not find any solution\n")
        f.write(f"chain break fraction: {chain_break_fraction}\n")

