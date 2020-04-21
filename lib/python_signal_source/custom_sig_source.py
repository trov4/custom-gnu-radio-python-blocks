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

    def __init__(self, frequency=10000, sample_frequency=20000):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='ASCII Shooter1',   # will show up in GRC
            in_sig=[np.complex64], # no input
            out_sig=[np.complex64]       # have a dummy output
        )
        self.freq = frequency
        self.samp_rate = long(sample_frequency)
        self.message_port_register_out(pmt.intern('freq'))  # port to send on

    def work(self, input_items, output_items):
        """example: multiply with constant"""

        time = 1.0/self.samp_rate
        f = 2*np.pi*self.freq
        for x in range(len(output_items[0])):
            t = x * time
            imag = np.sin(f*t)
            real = np.cos(f*t)
            output_items[0][x] = complex(real, imag)

        return len(output_items[0])
