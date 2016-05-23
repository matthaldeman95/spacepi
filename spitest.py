#!/usr/bin/env python


import time
import os
import sys
import RPi.GPIO as GPIO
import datetime
GPIO.setmode(GPIO.BCM)

def readAdc(adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(8, True)

        GPIO.output(11, False)  # start clock low
        GPIO.output(8, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(10, True)
                else:
                        GPIO.output(10, False)
                commandout <<= 1
                GPIO.output(11, True)
                GPIO.output(11, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(11, True)
                GPIO.output(11, False)
                adcout <<= 1
                if (GPIO.input(9)):
                        adcout |= 0x1

        GPIO.output(8, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
GPIO.setwarnings(False)

if __name__=='__main__':
	try:
		samples = 10000
		starttime = datetime.datetime.now()
		for n in range(0, samples):
			val0, val1, val2, val3 = readAdc(0), readAdc(1), readAdc(2), readAdc(3)
			#print readAdc(0)
		endtime = datetime.datetime.now()
		td = endtime-starttime
		time = td.total_seconds()
		print samples/time  
	except KeyboardInterrupt:
		GPIO.cleanup()
		sys.exit()           
