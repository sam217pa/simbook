import tskit

tc = tskit.TableCollection(1.0)

tc.nodes.add_row(flags=1, time=0.0)
tc.nodes.add_row(flags=1, time=0.0)
tc.nodes.add_row(flags=1, time=0.0)
tc.nodes.add_row(flags=1, time=0.0)
tc.nodes.add_row(flags=0, time=0.5)
tc.nodes.add_row(flags=0, time=1.0)

tc.edges.add_row(left=0, right=1, parent=4, child=0)
tc.edges.add_row(left=0, right=1, parent=4, child=1)
tc.edges.add_row(left=0, right=1, parent=4, child=2)
tc.edges.add_row(left=0, right=1, parent=5, child=3)
tc.edges.add_row(left=0, right=1, parent=5, child=4)

ts = tc.tree_sequence()
t = ts.first()
n = sorted([i for i in t.nodes()])
p = [t.parent(i) for i in n]
lc = [t.left_child(i) for i in n]
rc = [t.right_child(i) for i in n]
ls = [t.left_sib(i) for i in n]
rs = [t.right_sib(i) for i in n]
nl = {i: f"{i}:{p[i]},{lc[i]},{rc[i]},{ls[i]},{rs[i]}" for i in n}
t.draw(format='svg', path='nonbifurcating.svg',
       height=500, width=800, node_labels=nl)

