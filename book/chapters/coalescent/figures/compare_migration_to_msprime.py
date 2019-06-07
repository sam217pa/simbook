import msprime
import tskit
import numpy as np
import scipy.stats
import simbook.coalescent.migration as migration
from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

nreps = 10000
n0 = 10
n1 = 5
samples = ([i for i in range(n0)], [i for i in range(n0, n0+n1)])
windows = (0, 1)
migrate = 0.5

np.random.seed(35891235)
tmrca_simbook = np.zeros(nreps)
f2_simbook = np.zeros(nreps)

for i in range(nreps):
    ts = migration.simulate_two_demes(n0, n1, migrate)
    b = tskit.BranchLengthStatCalculator(ts)
    tmrca_simbook[i] = ts.tables.nodes.time.max()
    f2_simbook[i] = b.f2(samples, windows)[0][0]

tmrca_msprime = np.zeros(nreps)
f2_msprime = np.zeros(nreps)

config = [msprime.PopulationConfiguration(sample_size=n0),
          msprime.PopulationConfiguration(sample_size=n1)]
migmat = [[0, migrate/2.], [migrate/2., 0]]

for i, ts in enumerate(msprime.simulate(Ne=1, population_configurations=config,
                                        migration_matrix=migmat,
                                        num_replicates=nreps,
                                        random_seed=123235253)):
    tmrca_msprime[i] = 0.5*ts.tables.nodes.time.max()
    b = tskit.BranchLengthStatCalculator(ts)
    f2_msprime[i] = 0.5*b.f2(samples, windows)[0][0]

fig = plt.figure()
gs = gridspec.GridSpec(1, 2)
tmrca_ax = fig.add_subplot(gs[0])
f2_ax = fig.add_subplot(gs[1])
n, b, p = tmrca_ax.hist(tmrca_simbook, 100, density=True,
                        cumulative=True, histtype="step", label="simbook")
n, b, p = tmrca_ax.hist(tmrca_msprime, 100, density=True,
                        cumulative=True, histtype="step", label="msprime")
n, b, p = f2_ax.hist(f2_simbook, 100, density=True,
                     cumulative=True, histtype="step", label="simbook")
n, b, p = f2_ax.hist(f2_msprime, 100, density=True,
                     cumulative=True, histtype="step", label="simbook")
tmrca_ax.text(0.4, 0.5, "p = {:0.3f}".format(scipy.stats.ks_2samp(tmrca_msprime, tmrca_simbook)[1]),
              fontsize=12,
              horizontalalignment="left",
              transform=tmrca_ax.transAxes)
f2_ax.text(0.4, 0.5, "p = {:0.3f}".format(scipy.stats.ks_2samp(f2_msprime, f2_simbook)[1]),
           fontsize=12,
           horizontalalignment="left",
           transform=f2_ax.transAxes)

tmrca_ax.set_ylabel("Cumulative density")
plt.setp(f2_ax.get_yticklabels(), visible=False)
tmrca_ax.set_xlabel("TMRCA")
f2_ax.set_xlabel("F2")
tmrca_ax.legend(loc="lower right")
f2_ax.legend(loc="lower right")
plt.tight_layout()
plt.savefig("migration.png")
