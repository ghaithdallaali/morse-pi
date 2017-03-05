#!/usr/local/bin/python

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
            '-.--'  : 'Y',  '--..' : 'Z' ,
            
            # '0': '-----',  '1': '.----',  '2': '..---',
            # '3': '...--',  '4': '....-',  '5': '.....',
            # '6': '-....',  '7': '--...',  '8': '---..',
            # '9': '----.' 
        }

    for char in morse_code.split('/'):
        if char in CODE:
            print CODE[char.upper()],
#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    ambient_light = sum(ldr_readings(pin_to_circuit, 5))/5
    print "Calibrated! Ambient light is at %d" %ambient_light

    # print "Turn off the lights, Kathie!"
    # print "Now shine the light for 5 seconds on the LDR to calibrate it..."
    # time.sleep(5)
    # if (ldr_reading(pin_to_circuit)) < trigger:
    #     print "Calibrated!"
    #     time.sleep(1.5)
    # else:
    #     print "Calibration failed :("
    #     sys.exit()

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