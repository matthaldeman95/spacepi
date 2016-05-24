# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time
import datetime
import sys

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

outfile = open('testdata.csv','w')
outfile.write('time, adc0, adc1, adc2, adc3 \n')

while True:
	try:
		samples = 10000
		time = []
		val0, val1, val2, val3 = [],[],[],[]
		starttime = datetime.datetime.now()
		for n in range (0,samples):
			time.append(datetime.datetime.now())
			val0.append(mcp.read_adc(0))
			val1.append(mcp.read_adc(1))
			val2.append(mcp.read_adc(2))
			val3.append(mcp.read_adc(3))
			#print mcp.read_adc(0)
			#outfile.write('%s, %f, %f, %f, %f \n' % (datetime.datetime.now(),val0, val1, val2, val3))
		endtime = datetime.datetime.now()
		td = (endtime - starttime).total_seconds()
		print samples/td
		for m in range(0,len(val0)):
			outfile.write('%s, %d, %d, %d, %d \n'% (time[m],val0[m],val1[m],val2[m],val3[m]))
		outfile.write('\n \n \n \n \n')
	except KeyboardInterrupt:
		outfile.close()
		sys.exit()


