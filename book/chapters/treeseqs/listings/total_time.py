class TotalTime(object):
    def __init__(self):
        self.ttime = 0.0

    def process_outgoing(self, i, parent, ts):
        t = ts.tables.nodes.time[:]
        self.ttime -= t[parent[i]] - t[i]

    def process_incoming(self, i, parent, ts):
        t = ts.tables.nodes.time[:]
        self.ttime += t[parent[i]] - t[i]

    def get_result(self):
        return self.ttime
