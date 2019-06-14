import msprime
import numpy as np

nsam = 10
nreps = 10000
tmrca = np.zeros(nreps)

# The is the expectation in units of 2N generations
etmrca = 2.*(1. - 1./nsam)

# seed numpy
np.random.seed(666)

# 1. is the default value
for Ne in [1., 0.5, 0.25]:
    seed = np.random.randint(0, np.iinfo(np.uint32).max, size=1)
    for i, ts in enumerate(msprime.simulate(nsam, Ne=Ne,
                                            random_seed=seed,
                                            num_replicates=nreps)):
        tmrca[i] = ts.tables.nodes.time.max()
    print(f"Ne = {Ne}, mean TMRCA = {tmrca.mean():.4}, "
          f"Expectation = {etmrca*2.*Ne:.4}")
