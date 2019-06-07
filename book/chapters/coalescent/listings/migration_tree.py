import simbook.coalescent.migration as mig

ts = mig.simulate_two_demes(5, 5, 1)
# Label each node according
# to its population
pop = ts.tables.nodes.population[:]
nnodes = len(ts.tables.nodes)
nlabels = {i: "{}:{}".format(i, pop[i]) for i in range(nnodes)}
print(ts.first().draw(format="ascii", node_labels=nlabels))
