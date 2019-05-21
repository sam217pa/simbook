
def simulate(nsam: int):
    """
    The linear-time algorithm of Hudson, 1990,
    adapted to use tree sequences

    The citation for this algorithm is
    Hudson, Richard R. 1990.
    “Gene Genealogies and the Coalescent Process.”
    Oxford Surveys in Evolutionary Biology 7 (1): 44.

    Time is scaled in units of 2N generations.

    :param nsam: The sample size
    :type nsam: int
    """
    import tskit
    import numpy as np

    tc = tskit.TableCollection(1)

    nodes = np.arange(2*nsam - 1, dtype=np.int32)
    node_times = np.zeros(2*nsam - 1)
    num_edges = 2*nsam - 2
    parent = np.zeros(num_edges, dtype=np.int32)
    child = np.zeros(num_edges, dtype=np.int32)
    left = np.zeros(num_edges)
    right = np.ones(num_edges)
    next_node_time = nsam
    next_edge = 0
    time = 0.0

    n = nsam
    while n > 1:
        rcoal = (n*(n-1))/2.
        tcoal = np.random.exponential(1./rcoal)
        time += tcoal
        node_times[next_node_time] = time
        ancestor = 2*nsam - n
        p = np.random.choice(n, 1)[0]
        c1 = nodes[p]
        nodes[p] = nodes[n-1]
        p = np.random.choice(n-1, 1)[0]
        c2 = nodes[p]
        nodes[p] = nodes[2*nsam - n]
        if c1 > c2:
            c1, c2 = c2, c1
        parent[next_edge] = ancestor
        parent[next_edge+1] = ancestor
        child[next_edge] = c1
        child[next_edge+1] = c2
        next_node_time += 1
        next_edge += 2
        n -= 1
    tc.nodes.set_columns(time=node_times, flags=np.ones(
        len(node_times), dtype=np.uint32))
    tc.edges.set_columns(left=left, right=right,
                         parent=parent, child=child)

    return tc.tree_sequence()
