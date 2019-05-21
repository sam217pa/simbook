Hudson's linear-time algorithm
++++++++++++++++++++++++++++++++++++++++++++++++++++

.. literalinclude:: simbook/coalescent/hudson1990.py

Let's apply the function and print the tree:

.. ipython:: python

    from simbook.coalescent import hudson1990
    np.random.seed(42)
    ts = hudson1990.simulate(10)
    print(ts.first().draw(format="ascii"))

Let's get the distribution of TMRCA and the total time on the tree (TTOT):

.. ipython:: python

    nreps = 10000
    nsam = 50
    tmrca = np.zeros(nreps)
    ttot = np.zeros(nreps)
    for i in range(nreps):
        ts = hudson1990.simulate(nsam)
        tree = ts.first()
        ttot[i] = tree.total_branch_length
        tmrca[i] = ts.tables.nodes.time.max()

.. ipython:: python
    :suppress:

    fig = plt.figure()
    import matplotlib.gridspec as gridspec
    gs = gridspec.GridSpec(1, 2)
    tmrca_ax = fig.add_subplot(gs[0])
    ttot_ax = fig.add_subplot(gs[1],sharey=tmrca_ax)
    plt.setp(ttot_ax.get_yticklabels(), visible=False)
    etmrca = 2.*(1 - 1./nsam)
    ettot = 2.*(1./np.arange(1, nsam)).sum()
    tmrca_ax.set_xlabel("TMRCA")
    tmrca_ax.set_ylabel("Number of replicates")
    ttot_ax.set_xlabel("TTOT")
    tmrca_ax.text(0.3, 0.9, "Expected = {:0.2f}".format(etmrca),
       fontsize=12,
       horizontalalignment="left",
       transform=tmrca_ax.transAxes)
    tmrca_ax.text(0.3, 0.8, "Simulated = {:0.2f}".format(tmrca.mean()),
       fontsize=12,
       horizontalalignment="left",
       transform=tmrca_ax.transAxes)
    ttot_ax.text(0.3, 0.9, "Expected = {:0.2f}".format(ettot),
       fontsize=12,
       horizontalalignment="left",
       transform=ttot_ax.transAxes)
    ttot_ax.text(0.3, 0.8, "Simulated = {:0.2f}".format(ttot.mean()),
       fontsize=12,
       horizontalalignment="left",
       transform=ttot_ax.transAxes)
    tmrca_ax.axvline(x=etmrca, color="purple")
    ttot_ax.axvline(x=ettot, color="purple")
    n, bins, patches = ttot_ax.hist(ttot, 50)
    n, bins, patches = tmrca_ax.hist(tmrca, 50)
    @savefig hudson1990_tmrca_ttot.png width=6in
    plt.tight_layout();

Finally, an apples-to-apples comparison with msprime:

.. ipython:: python

    import msprime

    %%timeit
    hudson1990.simulate(100)

.. ipython:: python

    %%timeit
    msprime.simulate(100)

.. ipython:: python

    %%timeit 
    hudson1990.simulate(500)

.. ipython:: python

    %%timeit 
    msprime.simulate(500)

.. ipython:: python

    %%timeit 
    hudson1990.simulate(1000)

.. ipython:: python

    %%timeit 
    msprime.simulate(1000)
