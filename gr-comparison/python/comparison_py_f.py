#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
import time
import sys
import RPi.GPIO as GPIO
from gnuradio import gr

# TODO change names to some, normal, and secure, assign pins
led1_redpin = 11
led1_greenpin = 13
led2_redpin = 15
led2_greenpin = 12
led3_redpin = 16
led3_greenpin = 18

class comparison_py_f(gr.sync_block):
    """
    docstring for block comparison_py_f
    """
    def __init__(self, normal_threshold, secure_threshold):
        self.normal_threshold = normal_threshold
        self.secure_threshold = secure_threshold
        gr.sync_block.__init__(self,
            name="comparison_py_f",
            in_sig=[(numpy.float32,1250000)],
            out_sig=None)

    def on(pin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,GPIO.HIGH)

    def off(pin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,GPIO.LOW)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        samples = in0[0]

        num_samples = len(samples)

        # Initialize values for collection of stable runs of samples.
        stable_value = samples[0]
        stable_start = 0
        stable_length = 0
        stable_runs = [] # List of tuples (start index, length, value).

        # Collect list of add mode-length stable runs starting at 100k.
        for i in range(50000, num_samples):
            if abs(stable_value-samples[i]) < 2:
                stable_length += 1
            else:
                if stable_length >= 5000:
                    run = (stable_start, stable_length, stable_value)
                    stable_runs.append(run)
                stable_value = samples[i]
                stable_start = i
                stable_length = 0
        
        spike = [] # List of peak values between noise readings.
        spikes = [] # List of lists of peak values between noise readings.
        noise_value = -93
        last_noise = True
        noise = False
        spike_start = 0
        spike_end = 0

        # Find max power of each spike between noise readings.
        for tup in stable_runs:
            noise = abs(tup[2] - noise_value) < 5

            if not noise and last_noise:
                spike = []
                spike.append(tup[2])
                spike_start = tup[0]
            elif not noise and not last_noise:
                spike.append(tup[2])
            elif noise and not last_noise:
                spike_end = tup[0]
                total_spike_length = spike_end - spike_start
                if total_spike_length > 20000 and total_spike_length < 100000: # Append only add mode spikes.
                    spikes.append(spike)

            last_noise = noise

        add_mode_power = []

        for spike in spikes:
            add_mode_power.append(max(spike))

        if not add_mode_power:
            panel_power = noise_value
            print 'panel power level: no panel signal detected'
        else:
            panel_power = max(add_mode_power)
            print 'panel power level: %s' % (panel_power)

        normal = False
        secure = False
        some = False

        if panel_power > self.secure_threshold:
            secure = True
        if panel_power > self.normal_threshold:
            normal = True
        if panel_power > (noise_value+5):
            some = True

        if secure:
            print "secure"
	    	on(some_greenpin)
	    	on(normal_greenpin)
	    	on(secure_greenpin)
        elif normal:
            print "normal"
	    	on(some_greenpin)
	    	on(normal_greenpin)
	    	on(secure_redpin)
        elif some:
            print "some"
            on(some_greenpin)
	    	on(normal_redpin)
	    	on(secure_redpin)
        else:
            print "no signal detected"
			on(some_redpin)
			on(normal_redpin)
			on(secure_redpin)

		time.sleep(120)
		off(some_greenpin)
		off(some_redpin)
		off(normal_greenpin)
		off(normal_redpin)
		off(secure_greenpin)
		off(secure_redpin)

		# run button code on startup and never kill it
		# button press will
			# (re)start capture/measure code
			# turn off LEDs
			# maybe blink LEDs to indicate it's starting?

        return len(input_items[0])
