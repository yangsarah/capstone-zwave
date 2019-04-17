#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Osmocom Source
# Generated: Wed Feb 27 18:36:11 2019
##################################################

if __name__ == '__main__':
    import ctypes # foreign function library (provides C compatible types, allows calling function in DLLs)
    import sys # provides access to some vars used by interpreter, can find info about OS, etc
    if sys.platform.startswith('linux'): # if executing on a Linux system
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so') # load DLL for X11 (for graphics/UI)
            x11.XInitThreads() # initializes support for concurrent threads
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks # signal processing blocks
from gnuradio import eng_notation 
from gnuradio import filter # filter blocks
from gnuradio import gr # needed to run any GR apps
from gnuradio import wxgui # to create GUIs
from gnuradio.eng_option import eng_option # engineering notation for command line args
from gnuradio.filter import firdes # finite impulse response filter design functions
from gnuradio.wxgui import numbersink2 # graphical sink to display info
from grc_gnuradio import wxgui as grc_wxgui # more graphics
from optparse import OptionParser # parser for command line options
import osmosdr # SDR software
import time # time access and conversions
import wx # GUI toolkit
from multiply_py_ff import multiply_py_ff # newly created block


class osmocom_source(grc_wxgui.top_block_gui): # derived from top_block_gui, gives us functions to add and connect blocks

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Osmocom Source") # parent constructor
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY)) # icon for the GUI

        ##################################################
        # Variables
        ##################################################
        self.zwave_freq = zwave_freq = 908.42e6
        self.samp_rate = samp_rate = 3e6

        ##################################################
        # Blocks
        ##################################################

        # graphical number sink to display graph (path 1)
        self.wxgui_numbersink2_1 = numbersink2.number_sink_f(
        	self.GetWin(),
        	unit='Units',
        	minval=-100,
        	maxval=100,
        	factor=1.0,
        	decimal_places=10,
        	ref_level=0,
        	sample_rate=samp_rate,
        	number_rate=15,
        	average=False,
        	avg_alpha=None,
        	label='Number Plot',
        	peak_hold=False,
        	show_gauge=True,
        )
        self.Add(self.wxgui_numbersink2_1.win)

        # graphical number sink to display graph
        self.wxgui_numbersink2_0 = numbersink2.number_sink_f(
        	self.GetWin(),
        	unit='Units',
        	minval=-100,
        	maxval=100,
        	factor=1.0,
        	decimal_places=10,
        	ref_level=0,
        	sample_rate=samp_rate,
        	number_rate=15,
        	average=False,
        	avg_alpha=None,
        	label='Number Plot',
        	peak_hold=False,
        	show_gauge=True,
        )
        self.Add(self.wxgui_numbersink2_0.win)

        # source block: talks to airspy (both paths)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'airspy=0' )
        self.osmosdr_source_0.set_time_source('gpsdo', 0)
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(zwave_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(0, 0)
        self.osmosdr_source_0.set_if_gain(0, 0)
        self.osmosdr_source_0.set_bb_gain(0, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(20e4, 0)

        # low pass filter block to get rid of high frequency components (both paths)
        self.low_pass_filter_0 = filter.fir_filter_ccf(11, firdes.low_pass(
        	1, 256e3, 1e5, 5e4, firdes.WIN_HAMMING, 6.76))

        # root mean squared (path 2)
        self.blocks_rms_xx_0 = blocks.rms_cf(0.0001)

        # convert to dB scale (path 2)
        self._0 = blocks.nlog10_ff(20, 1, -14)

        # convert to dB scale (path 1)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 1, -15)

        # multiply by conjugate (path 1)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)

        # complex to real (path 1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)

        # new multiply all by 2 sink block
        self.multiply_py_ff = multiply_py_ff(2)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_complex_to_real_0, 0))    
        self.connect((self.blocks_nlog10_ff_0, 0), (self.wxgui_numbersink2_0, 0))    
        #self.connect((self.blocks_nlog10_ff_0_0, 0), (self.wxgui_numbersink2_1, 0))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.multiply_py_ff, 0)) # new
        self.connect((self.blocks_rms_xx_0, 0), (self.blocks_nlog10_ff_0_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_rms_xx_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.low_pass_filter_0, 0))   

    def get_zwave_freq(self):
        return self.zwave_freq

    def set_zwave_freq(self, zwave_freq):
        self.zwave_freq = zwave_freq
        self.osmosdr_source_0.set_center_freq(self.zwave_freq, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)


def main(top_block_cls=osmocom_source, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
