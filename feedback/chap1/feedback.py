import random

class Buffer:
    def __init__(self, max_wip, max_flow):
        self.queued = 0
        self.wip = 0 # work in progress
        self.max_wip = max_wip
        self.max_flow = max_flow

    def work(self, u):
        # Add to ready pool
        u = max(0, int(round(u)))
        u = min(u, self.max_wip))
        self.wip += u
        
        # Transfer from rady pool to queue
        r = int(round(random.uniform(0, self.max_flow)))
        self.wip -= r
        self.queued += r

        


class Controller


def open_loop():
    None


def closed_loop():
    None

c = Controller(1.25, 0.01)
p = Buffer(50, 10)

open_loop(p, 1000)
