.. _hudson1990:
   
Hudson's linear-time algorithm
++++++++++++++++++++++++++++++++++++++++++++++++++++

In a 1990 review article (:cite:`Hudson1990-ff`), Dick Hudson published the C
code for a linear time algorithm to simulate gene genealogies under the Kingman 
coalescent. His method works by realizing that for a sample of :math:`n` chromosomes,
the final tree with have :math:`2n - 1` nodes that we may label :math:`[0, 2n)`. 
The first :math:`n` nodes correspond to the present day sample, and the remaining
:math:`n-1` are the possible ancestors.  For example, if :math:`n = 4`, we have:

.. ipython:: python

    import numpy as np
    n = 4
    node_labels = np.arange(2*n - 1, dtype=np.int32)
    print(node_labels)

Our samples are:

.. ipython:: python

    print(node_labels[:n])

Our ancestral nodes are:

.. ipython:: python

    print(node_labels[n:])

More generally, at any time in the past where :math:`i` lineages remain,
the first :math:`i` nodes are represent the sample, and the remaining nodes
are their possible parents. We wish to take a random pair from the first :math:`i`
nodes and assign as their parent the first of the remaining possible ancestral nodes.

The algorithm to track the IDs of the remaining sample nodes proceeds as follows:

A. *Choose first sample node* Choose a value `p` uniformly from :math:`[1, i)` and record the node label at that position, *e.g.* set `c1 = node_labels[p]`.
B. *Update the sample list* Set `node_labels[c1] = node_labels[i-1]`, removing `c1` from the list of samples remaining.
C. *Choose second sample node* Choose `p` uniformly from :math:`[i, i-1)`, and set `c2 = node_labels[p]`. The swap in step B prevents `c1` from being chosen again.
D. *Update the sample list* Set `node_labels[c2] = node_labels[2*nsam - i]`. 
E. Set `i = i - 1`.  If `i == 1`, stop, otherwise return to A.

Step D is the tricky one.  It moves the first of the remaining ancestor IDs into the last position of
of the remaining sample IDs. At the end of this step, `node_labels[c2]`'s value is the ID of the
parent of `c1` and `c2`.

.. note::

   The above steps are the bulk of the C code under the comment
   "Generate the topology of the tree" in Hudson's paper.
   
The above algorithm is very straightforward to write out in vanilla
Python.  We also generate the tree corresponding to the simulated history.
The tree is represented as parent indexes. We also generate the time of 
the coalescent events.

.. ipython:: python

    def h1990(nsam):
       """
       Generate a coalescent tree using the 
       approach of Hudson, 1990.
       """
       node_labels = [i for i in range(2*nsam - 1)]
       tree = [-1 for i in range(2*nsam - 1)]
       tree[:nsam] = node_labels[:nsam]
       times = [0. for i in range(nsam)]
       print("Initial node list:",node_labels)
       i = nsam
       time = 0.0
       while i > 1:
          rcoal = (i*(i-1))/2. # Units of 2N generations
          tcoal = np.random.exponential(1./rcoal)
          time += tcoal
          times.append(time)
          p = np.random.choice(i, 1)[0] 
          c1 = node_labels[p] # Step A complete
          tree[c1] = 2*nsam - i
          node_labels[p] = node_labels[i-1] # Step B
          # Pick another of our remaining samples
          p = np.random.choice(i-1, 1)[0]
          c2 = node_labels[p] # Step C complete
          tree[c2] = 2*nsam - i
          # Swap our choice with an unused parental label
          node_labels[p] = node_labels[2*nsam - i] # Step D
          i -= 1
          print("After coalescing {} and {} into {}, sample list is: "\
             .format(c1,c2,node_labels[p]),node_labels[:i])
       return tree, times

.. note::

    A useful exercise would be to work out the difference in 
    how the tree structure is represented here compared to
    the code in :cite:`Hudson1990-ff`

Let's run the function, and look at the resulting tree structure:

.. ipython:: python

    np.random.seed(23456)
    tree, times = h1990(4)
    for i in range(7):
       print("node {}, parent {}, time {}".format(i,tree[i],times[i]))

The above code works and is very simple.  
The method is limited, though, as we have represented the tree using the classic
"list of indexes of parents" approach (CITATION).  A better approach would
be to modify the above algorithm to generate tree sequence data structures 
(see :cite:`Kelleher2016-cb` for details), which we do in the following code block,
which is part of the source code distributed with this book:

.. literalinclude:: ../../simbook/coalescent/hudson1990.py

The previous code block was used to generate the following plot:

.. plot:: chapters/coalescent/plots/h1990.py

    The distribution of the time to the most recent common ancestor (TMRCA) and the total time on the tree (TTOT) for a sample size of :math:`n = 50`. The distributions are based on 10,000 simulation replicates.
