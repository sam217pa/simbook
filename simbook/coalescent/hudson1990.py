import tskit
import numpy as np


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
    tc = tskit.TableCollection(1)

    nodes = np.arange(2*nsam - 1, dtype=np.int32)
    for i in range(nsam):
        tc.nodes.add_row(time=0.0, flags=tskit.NODE_IS_SAMPLE)
    time = 0.0
    n = nsam
    while n > 1:
        # Generate time to next coalescent event,
        # in units of 2N generations.
        rcoal = (n*(n-1))/2.
        tcoal = np.random.exponential(1./rcoal)
        time += tcoal

        # Register a new ancestor node.
        # The node is not a sample, 
        # so its flag is zero
        tc.nodes.add_row(time=time,
                         flags=0)
        # This is the index of the
        # ancestor node
        ancestor = 2*nsam - n

        # Perform the swap steps
        # of the algorithm
        p = np.random.choice(n, 1)[0]
        c1 = nodes[p]
        nodes[p] = nodes[n-1]
        p = np.random.choice(n-1, 1)[0]
        c2 = nodes[p]
        nodes[p] = nodes[ancestor]

        # Both c1 an c2 have the same parental
        # node (nodes[ancestor]).  An edge
        # table requires that child nodes
        # be sorted in increasing order
        # per parent, so we enforce that here
        if c1 > c2:
            c1, c2 = c2, c1
        # Record the edges
        tc.edges.add_row(parent=ancestor, child=c1,
                         left=0.0, right=1.0)
        tc.edges.add_row(parent=ancestor, child=c2,
                         left=0.0, right=1.0)
        n -= 1

    return tc.tree_sequence()
