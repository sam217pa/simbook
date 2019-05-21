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

.. plot:: coalescent/plots/h1990.py
