import msprime
from treewithrec import *

for i, t in enumerate(ts.trees()):
    nl = {j: f"{j}:{ts.tables.nodes[j].time:.4}" for j in t.nodes()}
    t.draw(format="svg",
           width=500, height=500,
           path=f"twotrees{i}.svg", node_labels=nl)
