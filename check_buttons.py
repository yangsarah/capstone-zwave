#!/usr/bin/env python3

from subprocess import call
import os
import time
import RPi.GPIO as GPIO

some_redpin = 17
some_greenpin = 2
normal_redpin = 26
normal_greenpin = 6
secure_redpin = 5
secure_greenpin = 25

power_button_pin = 3
take_reading_pin = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(power_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def on(pin):
        GPIO.output(pin,GPIO.HIGH)

def off(pin):
    GPIO.output(pin,GPIO.LOW)

def kill_reading():
    pid = 0
    processes = os.popen("ps a | grep 'python prog.py'").readlines()
    for process in processes:
        if process.split()[4] == 'python' and process.split()[5] == 'prog.py':
            pid = process.split()[0]
            break
    if(pid != 0):
        command = "kill -9 " + pid
        os.system(command)

def main():while True:
        # When power button pressed, turn off Pi.
        if not GPIO.input(power_button_pin):
            call(['shutdown', '-h', 'now'], shell=False)
            
        # When reading button pressed, turn off LEDs, blink LEDs, (re)start process.
        if not GPIO.input(take_reading_pin):
            kill_reading()
            off(some_greenpin)
            off(some_redpin)
            off(normal_greenpin)
            off(normal_redpin)
            off(secure_greenpin)
            off(secure_redpin)
            
            for i in range(0:3):
                on(some_greenpin)
                on(normal_greenpin)
                on(secure_greenpin)
                time.sleep(.25)
                off(some_greenpin)
                off(normal_greenpin)
                off(secure_greenpin)
                time.sleep(.25)
            
            call os.system("python take_reading.py &")
            
main()
