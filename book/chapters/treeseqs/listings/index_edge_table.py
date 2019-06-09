class EdgeTableIndex(object):
    def __init__(self, pos, t, p, c):
        self.position = pos
        self.time = t
        self.parent = p
        self.child = c

    def __str__(self):
        return str(f"position = {self.position:0.3}, "
                   f"time = {self.time:0.3}, "
                   f"parent = {self.parent}, "
                   f"child = {self.child}")


def index_edge_table(ts):
    I, O = [], []
    node_times = ts.tables.nodes.time[:]
    for e in ts.tables.edges:
        I.append(EdgeTableIndex(
            e.left, node_times[e.parent], e.parent, e.child))
        O.append(EdgeTableIndex(
            e.right, node_times[e.parent], e.parent, e.child))
    I = sorted(I, key=lambda x: (x.position, x.time, x.parent, x.child))
    O = sorted(O, key=lambda x: (x.position, -x.time, -x.parent, -x.child))
    return I, O
