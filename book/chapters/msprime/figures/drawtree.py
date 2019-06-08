import msprime

ts = msprime.simulate(10, random_seed=2636234)
nodes = ts.tables.nodes
node_times = {i: f"{nodes.time[i]:.2}" for i in range(len(nodes))}
ts.first().draw(format="svg", path="drawtree.svg",
                width=500, height=500,
                node_labels=node_times)
