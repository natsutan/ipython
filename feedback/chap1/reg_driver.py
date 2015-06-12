# -*- coding: utf-8 -*-
__author__ = 'natu'
from myhdl import *

def reg_driver_top(
        clk, reset,
        reg_kp, reg_ki,
        ):

    @instance
    def regDriver():
        while reset == 0:
            yield clk.posedge
        while reset == 1:
            yield clk.posedge

        reg_kp.next = 1.1
        reg_ki.next = 0.01
        yield clk.posedge


    return regDriver
