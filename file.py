import time
import datetime
import sys
from datetime import datetime
import gyro
import math as m

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

sensor = gyro.itg3200(1, 0x69, 0, 0)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

outfile = open('testdata.csv', 'w')
outfile.write('time, adc1, adc2, adc3, adc4, gx, gy, gz \n')

if __name__=="__main__":
    while True:
        try:
            samples = 10000
            t, gx, gy, gz = [], [], [], []
            val0, val1, val2, val3 = [], [], [], []
            starttime = datetime.now()
            for n in range(0,samples):
                t.append(datetime.now().time())
                val0.append(mcp.read_adc(0))
                val1.append(mcp.read_adc(1))
                val2.append(mcp.read_adc(2))
                val3.append(mcp.read_adc(3))
                if n%100 == 0:
                    gxval, gyval, gzval = sensor.read_data()
                gx.append(gxval)
                gy.append(gyval)
                gz.append(gzval)
            endtime = datetime.now()
            td = (endtime - starttime).total_seconds()
            print samples / td
            for m in range(0, len(val0)):
                outfile.write('%s, %d, %d, %d, %d, %f, %f, %f \n' % (t[m], val0[m], val1[m], val2[m], val3[m], gx[m], gy[m], gz[m]))
            outfile.write('\n \n \n \n \n')
	    time.sleep(2)
        except KeyboardInterrupt:
            outfile.close()
            sys.exit()
