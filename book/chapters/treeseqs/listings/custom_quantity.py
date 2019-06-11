def custom_quantity(ts, f):
    parent = np.array([-1]*len(ts.tables.nodes),
                      dtype=np.int32)

    maxpos = ts.get_sequence_length()
    i, o = 0, 0
    current_left = 0.0
    num_edges = len(ts.tables.edges)

    inorder, outorder = index_edge_table(ts)

    while i < num_edges or current_left < maxpos:
        while o < len(outorder) and \
                outorder[o].position == current_left:
            p = outorder[o].parent
            c = outorder[o].child
            f.process_outgoing(c, parent, ts)
            parent[c] = -1
            o += 1
        while i < num_edges and \
                inorder[i].position == current_left:
            p = inorder[i].parent
            c = inorder[i].child
            parent[c] = p
            f.process_incoming(c, parent, ts)
            i += 1
        right = maxpos
        if i < num_edges:
            right = min(right, inorder[i].position)
        if o < num_edges:
            right = min(right, outorder[o].position)
        yield f.get_result()

        current_left = right
