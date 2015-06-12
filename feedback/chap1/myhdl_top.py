# -*- coding: utf-8 -*-
__author__ = 'natu'
import random
from myhdl import Signal, delay, always, now, Simulation, instance, intbv, traceSignals, ResetSignal, toVerilog
#from feedback_hdl import feedback_top
from reg_driver import reg_driver_top


def run_sim():
#    inst = traceSignals(env)
    inst = env()
    sim = Simulation(inst)

    sim.run(40000000)

def env():
    # clk
    clk = Signal(bool(0))
    uClkDriver = ClkDriver(clk)
    reset = ResetSignal(0, active=True, async=True)

    uResetDriver = ResetDriver(clk, reset)

    # input port

    rin = Signal(intbv(0, min=0, max=256))
    gin = Signal(intbv(0, min=0, max=256))
    bin = Signal(intbv(0, min=0, max=256))
    radr = Signal(intbv(0, min=0, max=p_max_x * p_max_y))

    # output port
    rout = Signal(intbv(0, min=0, max=256))
    gout = Signal(intbv(0, min=0, max=256))
    bout = Signal(intbv(0, min=0, max=256))
    wadr = Signal(intbv(0, min=0, max=p_max_x * p_max_y))
    wen  = Signal(bool(0))

    # registers
    reg_kp = 0.0
    reg_ki = 0.0

    uRegDriver = reg_driver_top(
        clk, reset,
        reg_kp, reg_ki
        )


    uDut = smoother_top(
        clk, reset,
        rin, gin, bin, radr,
        rout, gout, bout, wadr, wen,
        reg_start, reg_end,
        reg_width, reg_height,
        reg_roi_x, reg_roi_y, reg_roi_h, reg_roi_w
    )


    return uClkDriver, uResetDriver, uRegDriver, uMem, uDut



def ClkDriver(clk, period = 20):
    lowTime = int(period/2)
    highTime = period - lowTime

    @instance
    def driveClk():
        while True:
            yield delay(lowTime)
            clk.next = 1
            yield delay(highTime)
            clk.next = 0

    return driveClk

def ResetDriver(clk, reset):
    lowTime = 2
    highTime = 1

    @instance
    def driveReset():
        reset.next = 0
        for i in range(lowTime):
            yield clk.posedge
        reset.next = 1
        for i in range(highTime):
            yield clk.posedge
        reset.next = 0
        yield clk.posedge

    return driveReset


def Buffer(clk, reset, max_wip, max_flow, u, queued):

    queued = 0
    wip = 0  # work in progress
    max_wip = max_wip
    max_flow = max_flow

    @instance
    def buffer():
        while(True):
            # Add to ready pool
            u = max(0, int(round(u)))
            u = min(u, max_wip)
            wip = wip + u

            # Transfer from raedy pool to queue
            r = int(round(random.uniform(0, wip)))
            wip -= r
            queued += r

            r = int(round(random.uniform(0, max_flow)))
            r = min(r, queued)
            queued.next -= r
            yield clk.posedge


    return buffer
