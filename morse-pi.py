#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
pin_to_circuit = 7

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

#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    print "Turn off the lights, Kathie!"
    print "Now shine the light for 5 seconds on the LDR to calibrate it..."
    time.sleep(5)
    if (ldr_reading(pin_to_circuit)) < 500:
        print "Calibrated!"
        time.sleep(1.5)
    else:
        print "Calibration failed :("
        sys.exit()

    morse_code = ""
    while True:
        if (ldr_reading(pin_to_circuit) < 500): 
            readings = [ldr_reading(pin_to_circuit), \
                        ldr_reading(pin_to_circuit), \
                        ldr_reading(pin_to_circuit), \
                        ldr_reading(pin_to_circuit)]
            for x in xrange(0,4):
                if (readings[x] < 500):
                    readings[x] = 1
                else:
                    readings[x] = 0
            if sum(readings) >= 3:
                morse_code+="_"
                sys.stdout.write('_')
                time.sleep(0.50)
            elif 1<= sum(readings) <= 2 :
                morse_code+="."
                sys.stdout.write('.')
                time.sleep(0.50)
        elif (ldr_reading(pin_to_circuit) > 200000) :
                morse_code+="/"
                sys.stdout.write('/')
                time.sleep(0.05)
        sys.stdout.flush()
except KeyboardInterrupt:
    print morse_code
    pass
finally:
    GPIO.cleanup()