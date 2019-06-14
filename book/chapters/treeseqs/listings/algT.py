import numpy as np


def algT(ts):
    """
    A re-implementation of Algorithm T
    from Kelleher et al (2016), PloS
    Compuational Biology,
    10.1371/journal.pcbi.1004842
    """
    parent = np.array([-1]*len(ts.tables.nodes),
                      dtype=np.int32)

    # The length of the genome
    maxpos = ts.get_sequence_length()
    i, o = 0, 0
    current_left = 0.0
    num_edges = len(ts.tables.edges)

    inorder, outorder = index_edge_table(ts)

    while i < num_edges or current_left < maxpos:
        # Remove parents from the tree
        while o < len(outorder) and \
                outorder[o].position == current_left:
            p = outorder[o].parent
            c = outorder[o].child
            parent[c] = -1
            o += 1
        # Add parents to the tree
        while i < num_edges and \
                inorder[i].position == current_left:
            p = inorder[i].parent
            c = inorder[i].child
            parent[c] = p
            i += 1
        # Get the right edge of the current tree
        right = maxpos
        if i < num_edges:
            right = min(right, inorder[i].position)
        if o < num_edges:
            right = min(right, outorder[o].position)
        # Send the current state of the tree
        # back to the calling environment
        yield current_left, parent

        # Update the left edge for the next
        # iteration through
        current_left = right
