import msprime
import numpy as np

config = [msprime.PopulationConfiguration(sample_size=10),
          msprime.PopulationConfiguration(sample_size=0)]
demographic_events = [msprime.MassMigration(time=0.1,
                                            source=0,
                                            destination=1,
                                            proportion=0.5),
                      msprime.MigrationRateChange(time=0.1,
                                                  rate=1e-2)]
ts = msprime.simulate(population_configurations=config,
                      demographic_events=demographic_events,
                      random_seed=462323)
# No recombination,
# so there is only one tree:
t = ts.first()
populations = ts.tables.nodes.population[:]
time = ts.tables.nodes.time[:]
node_labels = {i: f"{time[i]:0.3}" for i in t.nodes()}
colors = ["black", "red"]
node_colors = {i: colors[populations[i]] for i in t.nodes()}
t.draw(format="svg", path="popsplit.svg",
       node_labels=node_labels,
       # Note the mixing of British
       # and American English. :)
       node_colours=node_colors,
       height=500,  # unit is pixels
       width=600)
