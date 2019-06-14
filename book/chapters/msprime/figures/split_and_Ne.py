import msprime
import numpy as np
import matplotlib.pyplot as plt

nreps = 250
n, m1, m2, sem1, sem2 = [], [], [], [], []

np.random.seed(5125125)

for nsam in range(5, 135, 20):
    config = [msprime.PopulationConfiguration(sample_size=nsam),
              msprime.PopulationConfiguration(sample_size=nsam)]

    events = [msprime.MassMigration(time=0.025, source=1,
                                    dest=0, proportion=1.0)]

    nsing = np.zeros(nreps)
    seed = np.random.randint(0, np.iinfo(np.uint32).max, 1)

    for i, ts in enumerate(msprime.simulate(population_configurations=config,
                                            demographic_events=events,
                                            mutation_rate=50,
                                            random_seed=seed,
                                            num_replicates=nreps)):
        s = 0
        for v in ts.variants():
            if v.genotypes.sum() == 1:
                s += 1
        nsing[i] = s/ts.num_mutations

    events.append(msprime.PopulationParametersChange(time=0.025,
                                                     initial_size=2))

    nsing2 = np.zeros(nreps)
    seed = np.random.randint(0, np.iinfo(np.uint32).max, 1)

    for i, ts in enumerate(msprime.simulate(population_configurations=config,
                                            demographic_events=events,
                                            mutation_rate=50,
                                            random_seed=seed,
                                            num_replicates=nreps)):
        s = 0
        for v in ts.variants():
            if v.genotypes.sum() == 1:
                s += 1
        nsing2[i] = s/ts.num_mutations
    n.append(nsam)
    m1.append(nsing.mean())
    m2.append(nsing2.mean())
    sem1.append(nsing.std()/nreps)
    sem2.append(nsing2.std()/nreps)

fig = plt.Figure()
ax = plt.subplot()
ax.errorbar(n, m1, sem1, label="Constant "+r'$N_e$')
ax.errorbar(n, m2, sem2, label="Larger ancestral "+r'$N_e$')
ax.set_xlabel("Sample size in each present-day population")
ax.set_ylabel("Proportion of derived singletons " + r'$\pm SEM$')
plt.legend()
plt.tight_layout()
plt.savefig("splitscaling.png")
