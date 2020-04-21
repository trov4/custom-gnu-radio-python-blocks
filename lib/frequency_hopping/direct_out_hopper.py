"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

from __future__ import division
import numpy as np
from gnuradio import gr, blocks


# from datetime import datetime


from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import qtgui
import pmt
import time

from gnuradio import gr, gr_unittest
from gnuradio import blocks, analog
import numpy as np

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, base_frequency=10000, sample_frequency=100000, step_frequency = 1000, number_of_steps = 10):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Frequency Jumper',   # will show up in GRC
            in_sig=[np.complex64], # no input
            out_sig=[np.complex64]       # have a dummy output
        )
        self.freq = base_frequency
        self.base = base_frequency
        self.samp_rate = long(sample_frequency)
        self.message_port_register_out(pmt.intern('debug'))  # port to send on
        self.upper = step_frequency
        self.num = number_of_steps
        self.jumps = 0

        self.last_switch = time.time()

    def transition(self, t):
        now = time.time()
        if(now - self.last_switch > t):
            self.last_switch = time.time() 
            return True
        else:
            return False

    def work(self, input_items, output_items):
        """example: multiply with constant"""

        temp = 1.0/self.samp_rate
        f = 2*np.pi*self.freq
        for x in range(len(output_items[0])):
            time = x * temp
            imag = np.sin(f*time)
            real = np.cos(f*time)
            output_items[0][x] = complex(real, imag)

        if(self.transition(.4)):
            self.jumps = self.jumps + 1
            current = self.jumps%self.num
            self.freq = self.base + (self.upper*current)

        return len(output_items[0])
