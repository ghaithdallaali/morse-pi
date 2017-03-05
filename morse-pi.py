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
trigger = 500 # min threshhold before we record a dot/dash

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
            '-.--'  : 'Y',  '--..' : 'Z'
        }

    for char in morse_code.split('/'):
        if char in CODE:
            print CODE[char.upper()],
#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    ambient_light = sum(ldr_readings(pin_to_circuit, 5))/5
    print "Calibrated! Ambient light is at %d" %ambient_light

    morse_code = ""
    while True:
        if (ldr_reading(pin_to_circuit) < trigger): 
            readings = ldr_readings(pin_to_circuit,4)
            for x in xrange(0,4):
                if (readings[x] < trigger):
                    readings[x] = 1
                else:
                    readings[x] = 0
            if sum(readings) >= 3:
                morse_code+="-"
                sys.stdout.write('-')
                time.sleep(0.50)
            elif 1<= sum(readings) <= 2 :
                morse_code+="."
                sys.stdout.write('.')
                time.sleep(0.50)
        elif (ldr_reading(pin_to_circuit) >= (ambient_light + 50)) :
                morse_code+="/"
                sys.stdout.write('/')
                time.sleep(0.70)
        sys.stdout.flush()
except KeyboardInterrupt:
    print "\n"
    morse_translator(morse_code)
    pass
finally:
    GPIO.cleanup()
