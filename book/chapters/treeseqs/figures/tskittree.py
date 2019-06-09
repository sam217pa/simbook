import msprime

ts = msprime.simulate(5, random_seed=42)
nl = {i: f"{i}:{ts.tables.nodes[i].time:.2}" for i in range(
    len(ts.tables.nodes))}
ts.first().draw(format="svg",
                width=500, height=500,
                path="tskittree.svg", node_labels=nl)
