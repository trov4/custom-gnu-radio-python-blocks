"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

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





class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, base_freq=5800000000, number_freq=70, bandwidth=1000000):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Frequency Jumper',   # will show up in GRC
            in_sig=None,#[np.complex64], # no input
            out_sig=[np.complex64]       # have a dummy output
        )

        self.curr_increment = 0                             # adds to base_freq
        self.total_out = number_freq                        # 70 
        self.increment = bandwidth * 100                    # increment by bandwidth needs some offput (tbd on why)
        self.base_freq = base_freq
        self.curr_out = self.base_freq                      # start at base frequency
        self.message_port_register_out(pmt.intern('freq'))  # port to send on
    
    def wait(self, t):
        start = time.time()
        now = time.time()
        while now-start < t:
            now=time.time()

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        # send signal (register port, PMT message)
        self.message_port_pub(pmt.intern('freq'),  pmt.from_double(long(self.curr_out)))
        #wait
        self.wait(.4)  #.4 seconds
        # update counter
        if self.curr_increment > 69:
            self.curr_increment = -1
        self.curr_increment = self.curr_increment + 1
        # update output
        self.curr_out = self.base_freq + self.curr_increment*self.increment
        return 1