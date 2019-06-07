import numpy as np


def h1990(nsam):
    """
    Generate a coalescent tree using the 
    approach of Hudson, 1990.
    """
    node_labels = [i for i in range(2*nsam - 1)]
    tree = [-1 for i in range(2*nsam - 1)]
    tree[:nsam] = node_labels[:nsam]
    times = [0. for i in range(nsam)]
    print("Initial node list:", node_labels)
    i = nsam
    time = 0.0
    while i > 1:
        rcoal = (i*(i-1))/2.  # Units of 2N generations
        tcoal = np.random.exponential(1./rcoal)
        time += tcoal
        times.append(time)
        p = np.random.choice(i, 1)[0]
        c1 = node_labels[p]  # Step A complete
        tree[c1] = 2*nsam - i
        node_labels[p] = node_labels[i-1]  # Step B
        # Pick another of our remaining samples
        p = np.random.choice(i-1, 1)[0]
        c2 = node_labels[p]  # Step C complete
        tree[c2] = 2*nsam - i
        # Swap our choice with an unused parental label
        node_labels[p] = node_labels[2*nsam - i]  # Step D
        i -= 1
        print("After coalescing {} and {} into {}, sample list is: "
              .format(c1, c2, node_labels[p]), node_labels[:i])
    return tree, times
