__author__ = 'natutan'


from myhdl import *

def controller_top(
        clk, reset,
        kp, ki, e,
        out,
    ):

    i = 0

    @always_seq(clk.posedge, reset=reset)
    def fsm():
        global i
        if reset == 1:
            out.next = 0
            i = 0
        else:
            i = i +  e
            out.next = kp * e + ki * i


    return fsm
