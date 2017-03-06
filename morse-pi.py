#!/usr/local/bin/python

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# 

# This application converts light incident to an LDR to Morse 
# code dits and dahs before translating them. See README.md 
# for more information
#
# @author Ghaith Dalla-Ali  

import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
pin_to_circuit = 7 # pin ldr is connected to
trigger_tol = 250
ambient_light_tol = 300
num_readings = 4
delimiter = '/'
dit = '.'
dah = '-'

def ldr_reading (pin_to_circuit):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.10)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count

def ldr_readings (pin_to_circuit, num_readings):
    readings = []
    for x in xrange(0,num_readings):
        readings.append(ldr_reading(pin_to_circuit))
    
    # print "readings is %s" %readings ;# GHAITH DEBUG
    return readings

def morse_translator (morse_code):
    CODE = {'.-'    : 'A',  '-...' : 'B' ,    '-.-.'    : 'C' ,
            '-..'   : 'D',  '.'    : 'E' ,    '..-.'    : 'F' ,
            '--.'   : 'G',  '....' : 'H' ,    '..'      : 'I' ,
            '.---'  : 'J',  '-.-'  : 'K' ,    '.-..'    : 'L' ,
            '--'    : 'M',  '-.'   : 'N' ,    '---'     : 'O' ,
            '.--.'  : 'P',  '--.-' : 'Q' ,    '.-.'     : 'R' ,
            '...'   : 'S',  '-'    : 'T' ,    '..-'     : 'U' ,
            '...-'  : 'V',  '.--'  : 'W' ,    '-..-'    : 'X' ,
            '-.--'  : 'Y',  '--..' : 'Z' ,    '.....'   : ' ' ,
        }

    for char in morse_code.split(delimiter):
        if char in CODE:
            print '\033[93m' + CODE[char.upper()],
#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    ambient_light = sum(ldr_readings(pin_to_circuit, num_readings))/num_readings
    print "Calibrated! Ambient light is at %d" %ambient_light
    trigger = ambient_light - trigger_tol
    # print "trigger:" + str(trigger) + " ambient_light:" + str(ambient_light) ;# GHAITH DEBUG
    morse_code = ""
    while True:
        if (ldr_reading(pin_to_circuit) <= trigger): 
            readings = ldr_readings(pin_to_circuit,num_readings)
            for x in xrange(0,num_readings):
                if (readings[x] <= trigger):
                    readings[x] = 1
                else:
                    readings[x] = 0
            if sum(readings) >= (num_readings - 1):
                morse_code+=dah
                sys.stdout.write(dah)
                time.sleep(0.50)
            elif 1 <= sum(readings) <= (num_readings/2) :
                morse_code+=dit
                sys.stdout.write(dit)
                time.sleep(0.50)
        elif (ldr_reading(pin_to_circuit) >= (ambient_light + ambient_light_tol)) :
                morse_code+=delimiter
                sys.stdout.write(delimiter)
                time.sleep(0.70)
        sys.stdout.flush()
except KeyboardInterrupt:
    print "\n\n"
    morse_translator(morse_code)
    print "\n\n"
    pass
finally:
    GPIO.cleanup()
