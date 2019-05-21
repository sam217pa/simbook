
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

    for i in range(nsam):
        tc.nodes.add_row(time=0, flags=1)

    nodes = np.arange(2*nsam - 1, dtype=np.int32)
    time = 0.0

    n = nsam
    while n > 1:
        rcoal = (n*(n-1))/2.
        tcoal = np.random.exponential(1./rcoal)
        time += tcoal
        tc.nodes.add_row(time=time)
        ancestor = 2*nsam - n
        p = np.random.choice(n, 1)[0]
        c1 = nodes[p]
        nodes[p] = nodes[n-1]
        p = np.random.choice(n-1, 1)[0]
        c2 = nodes[p]
        nodes[p] = nodes[2*nsam - n]
        if c1 > c2:
            c1, c2 = c2, c1
        tc.edges.add_row(left=0., right=1.,
                         parent=ancestor, child=c1)
        tc.edges.add_row(left=0., right=1.,
                         parent=ancestor, child=c2)
        n -= 1

    return tc.tree_sequence()
