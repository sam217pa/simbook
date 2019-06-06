import numpy as np
import simbook.coalescent.hudson1990 as hudson1990
from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
rc('font', **{'size': 18})

nreps = 10000
nsam = 50
tmrca = np.zeros(nreps)
ttot = np.zeros(nreps)
for i in range(nreps):
    ts = hudson1990.simulate(nsam)
    tree = ts.first()
    ttot[i] = tree.total_branch_length
    tmrca[i] = ts.tables.nodes.time.max()

fig = plt.figure()
gs = gridspec.GridSpec(1, 2)
tmrca_ax = fig.add_subplot(gs[0])
ttot_ax = fig.add_subplot(gs[1], sharey=tmrca_ax)
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
plt.tight_layout()
plt.savefig('hudson1990.png')
