import random
import pylab

MAX_DATA = 1000
rs = [0] * MAX_DATA
es = [0.0] * MAX_DATA
us = [0.0] * MAX_DATA
ys = [0] * MAX_DATA


class Buffer:
    def __init__(self, max_wip, max_flow):
        self.queued = 0
        self.wip = 0  # work in progress
        self.max_wip = max_wip
        self.max_flow = max_flow

    def work(self, u):
        # Add to ready pool
        u = max(0, int(round(u)))
        u = min(u, self.max_wip)
        self.wip += u
        
        # Transfer from raedy pool to queue
        r = int(round(random.uniform(0, self.wip)))
        self.wip -= r
        self.queued += r

        r = int(round(random.uniform(0, self.max_flow)))
        r = min(r, self.queued)
        self.queued -= r

        return self.queued


class Controller:
    def __init__(self, kp, ki):
        self.kp = kp
        self.ki = ki
        self.i = 0  # Cumulative error

    def work(self, e):
        self.i += e
        return self.kp*e + self.ki*self.i


def open_loop(p, tm = 5000):
    def target(t):
        return 5.0 # 5.1

    for t in range(tm):
        u = target(t)
        y = p.work(u)


def closed_loop(c, p, tm = 5000):
    global rs, es, us, ys

    def set_point(t):
        if t < 100: return 0
        if t < 300: return 50
        return 10

    y = 0
    for t in range(tm):
        r = set_point(t)
        e = r - y
        u = c.work(e)
        y = p.work(u)

        #print t, r, e, u, y
        print("%d %d %f %f %d" % (t, r, e, u, y))
        rs[t], es[t], us[t], ys[t] = r, e, u, y

def plot(fname):
    pylab.figure()
    pylab.plot(rs, 'b.-')
    pylab.plot(us, 'y.-')
    pylab.plot(ys, 'r.-')

    pylab.savefig("chap1.png")
    pylab.show()

#c = Controller(1.25, 0.01)
#p = Buffer(50, 10)
#open_loop(p, 1000)

c = Controller(1.10, 0.01)
p = Buffer(50, 10)

closed_loop(c, p, MAX_DATA)
plot("result.png")
