"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!

Author: Trevor Stanca
contact: tstanca@students.kennesaw.edu
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
import array

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, base_frequency=1e3, sample_rate=20e6, step_frequency = 1e6, string='---n--', t=.4):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='ASCII Shooter1',   # will show up in GRC
            in_sig=None, #[np.complex64], # no input
            out_sig=[np.complex64]       # have a dummy output
        )
        self.base = base_frequency
        self.samp_rate = float(sample_rate)
        self.message_port_register_out(pmt.intern('freq'))  # port to send on
        self.upper = step_frequency
        self.t = t
        self.last_switch = time.time()
        self.string = string

        self.init_arrays()
        self.currY = 0
        self.proceed = True

    def init_arrays(self):
        array = np.array([[False, False, False],[False, False, False], [False, False, False]])
        # -
        self.dash = np.array([[False, False, False],[True, True, True], [False, False, False]])

        # | 
        self.pip = np.array([[False, True, False], [False, True, False], [False, True, False]])

        # \
        self.back_slash = np.array([[True, False, False],[False, True, False], [False, False, True]])

        # /
        self.slash = np.array([[False, False, True],[False, True, False], [True, False, False]])

        # .
        self.period = np.array([[False, False, False],[False, False, False], [False, True, False]])

        # _
        self.under_score = np.array([[False, False, False],[False, False, False], [True, True, True]])

        # '
        self.single_quote = np.array([[False, True, False],[False, False, False], [False, False, False]])

        # <
        self.less_than = np.array([[False, False, True],[False, True, False], [False, False, True]])

        # >
        self.greater_than = np.array([[True, False, False],[False, True, False], [True, False, False]])

        # * (spelling?)
        self.astricts = np.array([[False, False, False],[False, True, False], [False, False, False]])

        # ^
        self.carrot = np.array([[True, False, True],[False, True, False], [False, False, False]])

        # (
        self.left_paren = np.array([[False, True, False],[True, False, False], [False, True, False]])

        # )
        self.right_paren =np.array([[True, False, False],[False, True, False], [True, False, False]])

        # space/not in the list above
        self.default = array

    def grab_array(self, char, row):
        if char == '-':
            # self.message_port_pub(pmt.intern('freq'), pmt.from_double(0))
            return self.dash[row]
        elif char == '|':
            # self.message_port_pub(pmt.intern('freq'), pmt.from_double(1))
            return self.pip[row]
        elif char=='\\':
            return self.back_slash[row]
        elif char=='/':
            return self.slash[row]
        elif char == '.':
            return self.period[row]
        elif char == '_':
            return self.under_score[row]
        elif char == '\'':
            return self.single_quote[row]
        elif char == '<':
            return self.less_than[row]
        elif char == '>':
            return self.greater_than[row]
        elif char == '*':
            return self.astricts[row]
        elif char == '^':
            return self.carrot[row]
        elif char == '(':
            return self.left_paren[row]
        elif char == ')':
            return self.right_paren[row]
        else:
            return np.array([False for x in xrange(3)])


    def transition(self, t):
        now = time.time()
        if(now - self.last_switch > t):
            self.last_switch = time.time() 
            return True
        else:
            return False

    def work(self, input_items, output_items):
        # self.init_arrays()
        """example: multiply with constant"""
        #test code
        # f1 = 2*np.pi*1e6
        # # f2 = 4*np.pi*self.base
        # time = 1.0/self.samp_rate
        # for a in range(len(output_items[0])):
        #     for x in range(7):
        #         real = np.cos(f1*time*a*x)
        #         imag = np.sin(f1*time*a*x)
        #         output_items[0][a] = output_items[0][a] + complex(real, imag)#np.complex64(real + imag*1j)

        output_items[0][:] = 0
        if self.proceed:
            for a in range(len(output_items[0])):
                time = float(a/self.samp_rate)
                x = 0
                c = 0
                while (self.string[c] != 'n'):
                    array = self.grab_array(self.string[c], self.currY)
                    for b in range(len(array)):
                        if array[b]:
        	            	freq = (self.upper*x)
        	                f = 2*np.pi*freq
        	                imag = np.sin(f*time)*array[b]
        	                real = np.cos(f*time)*array[b]
        	                output_items[0][a] = output_items[0][a] + complex(real, imag)
                        x = x + 1
                    c = c + 1


        if(self.transition(self.t)):
            self.currY = (self.currY + 1) % 3
            a = 0
            while self.string[a] != 'n':
                a = a + 1
            if self.currY == 0:
                if a+1 >= len(self.string):
                    self.proceed = False
                else:
                    self.string = self.string[a+1:]
        return len(output_items[0])