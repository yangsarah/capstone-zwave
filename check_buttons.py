#!/usr/bin/env python3

from subprocess import call
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
GPIO.setup(take_reading_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(some_redpin, GPIO.OUT)
GPIO.setup(some_greenpin, GPIO.OUT)
GPIO.setup(normal_redpin, GPIO.OUT)
GPIO.setup(normal_greenpin, GPIO.OUT)
GPIO.setup(secure_redpin, GPIO.OUT)
GPIO.setup(secure_greenpin, GPIO.OUT)

def on(pin):
    GPIO.output(pin,GPIO.HIGH)

def off(pin):
    GPIO.output(pin,GPIO.LOW)

def kill_reading():
    pid = 0
    processes = os.popen("ps aux | grep 'python2 /home/pi/Documents/capstone-zwave/take_reading.py'").readlines()
    for process in processes:
        if process.split()[10] == 'python' and process.split()[11] == '/home/pi/Documents/capstone-zwave/take_reading.py':
            pid = process.split()[1]
            break
    if(pid != 0):
        command = "kill -9 " + pid
        os.system(command)

def main():
    while True:
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
            
            for i in range(3):
                on(some_greenpin)
                on(normal_greenpin)
                on(secure_greenpin)
                time.sleep(.20)
                off(some_greenpin)
                off(normal_greenpin)
                off(secure_greenpin)
                time.sleep(.1)
            
            call(['python', '/home/pi/Documents/capstone-zwave/take_reading.py'], shell=False)
            
main()
