__author__ = 'natutan'


from myhdl import *

def controller_top(
        clk, reset,
        e,
        reg_kp, reg_ki,
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
            out.next = reg_kp * e + reg_ki * i


    return fsm
