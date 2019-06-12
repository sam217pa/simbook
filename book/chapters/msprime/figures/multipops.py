import msprime

config = [msprime.PopulationConfiguration(sample_size=5),
          msprime.PopulationConfiguration(sample_size=5)]
demographic_events = [msprime.MassMigration(time=3.0,
                                            source=1,
                                            destination=0,
                                            proportion=1.0)]
ts = msprime.simulate(population_configurations=config,
                      demographic_events=demographic_events,
                      random_seed=987654321)
# No recombination,
# so there is only one tree:
t = ts.first()
populations = ts.tables.nodes.population[:]
time = ts.tables.nodes.time[:]
node_labels = {i: f"{time[i]:0.3}" for i in t.nodes()}
colors = ["black", "red"]
node_colors = {i: colors[populations[i]] for i in t.nodes()}
t.draw(format="svg", path="multipops.svg",
       node_labels=node_labels,
       # Note the mixing of British
       # and American English. :)
       node_colours=node_colors,
       height=500,  # unit is pixels
       width=600)
