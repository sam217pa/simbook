import msprime
import numpy as np
import scipy.stats
from matplotlib import rc
import matplotlib.pyplot as plt

nreps = 10000

nmuts1 = np.zeros(nreps)
nmuts2 = np.zeros(nreps)

for i, ts in enumerate(msprime.simulate(10, mutation_rate=25.0,
                                        num_replicates=nreps,
                                        random_seed=3152512)):
    nmuts1[i] = ts.num_mutations

for i, ts in enumerate(msprime.simulate(10, mutation_rate=0.25,
                                        Ne=100,
                                        num_replicates=nreps,
                                        random_seed=3152512)):
    nmuts2[i] = ts.num_mutations

fig = plt.figure()
n, b, p = plt.hist(nmuts1, 100, density=True,
                   cumulative=True, histtype="step", label=r'$N_e = 1$')

n, b, p = plt.hist(nmuts2, 100, density=True, ls='dashed',
                   cumulative=True, histtype="step", label=r'$N_e = 100$')
plt.legend(loc="lower right")
plt.xlabel("Number of mutations")
plt.tight_layout()
plt.savefig("msprime_scaling.png")
