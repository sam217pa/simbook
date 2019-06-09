import msprime

ts = msprime.simulate(5, random_seed=6436236)
t = ts.first()
n = sorted([i for i in t.nodes()])
p = [t.parent(i) for i in n]
lc = [t.left_child(i) for i in n]
rc = [t.right_child(i) for i in n]
ls = [t.left_sib(i) for i in n]
rs = [t.right_sib(i) for i in n]
nl = {i: f"{i}:{p[i]},{lc[i]},{rc[i]},{ls[i]},{rs[i]}" for i in n}
t.draw(format='svg', path='smalltree.svg',
       height=500, width=800, node_labels=nl)
