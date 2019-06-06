.. _migration:

The coalescent with migration   
++++++++++++++++++++++++++++++++++++++++++++++++++++

In this section, we extend the algorithm to allow for symmetric migration between two discrete demes.  This is the
standard "island model" of migration (CITATION). 

With population structure, two lineages may only coalesce if they are both present in the same deme.  Migration events
change the label of a deme.  Thus, we must track the current number of lineages in each deme.  This additional
requirement substantially increases the complexity of the simulation, as we now have the following possible events:

1. Coalescence in deme 0
2. Coalescence in deme 1
3. Migration from deme 0 to deme 1
4. Migration from deme 1 to deme 0

For simplicty, we assume:

1. The migration rate from deme zero to one equals the rate from one to zero.
2. The effective size each deme is the same.

Define :math:`m` as the rate (per :math:`2N` generations) at which a lineage migrates to the other deme, where :math:`N` is the effective size of a deme. 
At any time in the past, there are :math:`n_0` lineages remaining in deme zero and :math:`n_1` remaining in deme one.
The migration rate per :math:`2N` generation from deme zero to deme one is :math:`mn_0`, and the rate in the reverse
direction is :math:`mn_1`.  The total migration rate is therefore :math:`M=m(n_0+n_1)`, and the mean time to the next migration event is
exponentially-distributed with mean :math:`1/M`.  Likewise, the rates of coalscence in the demes are
:math:`{n_0 \choose 2}` and :math:`{n_1 \choose 2}`, respectively, and the total rate of coalscence is the sum of the
two rates.

To get the time to the next event, we have several options. For example, we could draw the next time for each of the four possible events
and the minimum value determines the event.  This method would give the correct results but would be relatively
inefficient, as exponential deviates are one of the more expensive to generate.

A more efficient method is to generate the time to the next migration event (mean :math:`1/M` time units), and the time
to the next coalescent event (mean :math:`1/\left[{n_0 \choose 2} + {n_1 \choose 2}\right]` time units).  If the time to the next
migration event is the smaller of the two, we chose the deme proportional to the sample size within each deme.  If the
time to the next coalescent event is the smaller value, we choose deme proportional to their rates of coalscence.

The following listing shows the algorithm for the case of two demes:

.. literalinclude:: ../../simbook/coalescent/migration.py

Let's look at some output:

.. ipython:: python

    import IPython
    import simbook.coalescent.migration as mig

    ts = mig.simulate_two_demes(5,5,1)
    # Label each node according 
    # to its population
    pop = ts.tables.nodes.population[:]
    nnodes = len(ts.tables.nodes)
    nlabels = {i:"{}:{}".format(i,pop[i]) for i in range(nnodes)}
    print(ts.first().draw(format="unicode", node_labels=nlabels))

In the above tree, a mutation on any internal node leading to descendants in both demes will be a shared polymorphism.
A mutation on a node leading only to samples from one population results in a private polymorphism or a fixed difference 
between demes.  The relative number of shared, private, and fixed mutations determines the value of summaries of
differentiation such as :math:`F_{st}` and the :math:`f` statistics from :cite:`Patterson2012-sw`.

The following plot compares the output from our simulation to the output from `msprime`:

.. plot:: chapters/coalescent/plots/compare_migration_to_msprime.py

      The empirical cumulative density function (ECDF) of TMRCA and the :math:`f_2` statistic (:cite:`Patterson2012-sw`) in a model of symmetric migration between two demes of equal size.  The initial sample sizes in each deme are 10 and 5.  The total migration rate (per lineage per 2N generations) is 0.5, and migration rates are symmetric between demes.  The comparison to `msprime` is based on 10,000 replicates and accounts for the difference in time scale between the two implementations. The sudden drop to zero at the right of each panel is a side-effect of plotting ECDF functions using matplotlib.

.. todo::

   Discuss how multiple demes, changing deme size, etc., all affect things.
