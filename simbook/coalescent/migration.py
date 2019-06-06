import numpy as np
import tskit


def _get_rates(config, migrate):
    rcoal0 = (config[0]*(config[0]-1))/2.
    rcoal1 = (config[1]*(config[1]-1))/2.
    rcoal = rcoal0+rcoal1
    total_n = config.sum()
    if rcoal > 0.:
        tcoal = np.random.exponential(1./rcoal)
    else:
        tcoal = np.finfo(np.float).max
    if migrate > 0.:
        tmig = np.random.exponential(1./(total_n*migrate))
    else:
        tmig = np.finfo(np.float).max
    return tcoal, tmig, rcoal0, rcoal1


def _pick_migrant(config):
    p0 = config[0]/(config[0] + config[1])
    if np.random.uniform() < p0:
        return 0, 1
    return 1, 0


def simulate_two_demes(n0, n1, migrate):
    if n0 < 0 or n1 < 0:
        raise ValueError("sample sizes must be >= 0")
    nsam = n0 + n1
    if nsam < 2:
        raise ValueError("total sample size must be > 1")

    tc = tskit.TableCollection(1)

    for i in range(n0):
        tc.nodes.add_row(time=0.0,
                         flags=tskit.NODE_IS_SAMPLE, population=0)
    for i in range(n1):
        tc.nodes.add_row(time=0.0,
                         flags=tskit.NODE_IS_SAMPLE, population=1)
    for i in range(2):
        tc.populations.add_row()

    nodes = np.arange(2*nsam - 1, dtype=np.int32)
    time = 0.0
    total_n = nsam
    config = np.array([n0, n1], dtype=np.int32)
    current_demes = np.array([-1] * len(nodes), dtype=np.int32)
    current_demes[:n0] = 0
    current_demes[n0:nsam] = 1

    while total_n > 1:
        tcoal, tmig, rcoal0, rcoal1 = _get_rates(config, migrate)

        if tmig < tcoal:
            time += tmig
            source, dest = _pick_migrant(config)
            idx = np.where(current_demes == source)[0]
            p = np.random.choice(len(idx), 1)[0]
            current_demes[idx[p]] = dest
            config[source] -= 1
            config[dest] += 1
        else:
            time += tcoal
            if np.random.uniform() < rcoal0/(rcoal0 + rcoal1):
                deme = 0
            else:
                deme = 1
            tc.nodes.add_row(time=time, flags=0, population=deme)
            ancestor = 2*nsam - total_n
            idx = np.where(current_demes == deme)[0]
            p = np.random.choice(len(idx), 1)[0]
            c1 = nodes[idx[p]]
            assert current_demes[idx[p]] == deme
            nodes[idx[p]] = nodes[idx[-1]]
            current_demes[idx[-1]] = -1
            p = np.random.choice(len(idx)-1, 1)[0]
            assert current_demes[idx[p]] == deme
            c2 = nodes[idx[p]]
            nodes[idx[p]] = ancestor
            if c1 > c2:
                c1, c2 = c2, c1
            tc.edges.add_row(parent=ancestor, child=c1,
                             left=0.0, right=1.0)
            tc.edges.add_row(parent=ancestor, child=c2,
                             left=0.0, right=1.0)
            config[deme] -= 1
            total_n -= 1
    return tc.tree_sequence()
