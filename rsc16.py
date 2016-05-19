import spidev
from datetime import datetime
import sys
import gyro
import time
import spilib
import math as m

sensor = gyro.itg3200(1, 0x69, 0, 0)
spi = spidev.SpiDev()
spi.open(0,0);
spi.max_speed_hz = 32000000

"""
USER INPUTS
"""

gyrothreshold = 200
totalrecordtime = 30
sleeptime = 5

print "Sleeping..."
time.sleep(sleeptime)

outfile = open('testdata.csv', 'w')
outfile.write('time, adc1, adc2, adc3, adc4, gx, gy, gz \n')


def checkgyro(gyrothreshold):
    gx, gy, gz = sensor.read_data()
    print "Checking gyro threshold:", gx, gy, gz
    while m.fabs(gz) < gyrothreshold:
        time.sleep(3)
        gx, gy, gz = sensor.read_data()
	print "Checking gyro threshold:", gx, gy, gz
    time.sleep(3)
    gx, gy, gz = sensor.read_data()
    if m.fabs(gz) < 1000:
        checkgyro(gyrothreshold)
    else: return

def datawrite(outfile):
    print "Recording data now"
    for n in range(0,10000):
        val0,val1,val2,val3 = spilib.readAdc(spi,0), spilib.readAdc(spi,1), spilib.readAdc(spi,2), spilib.readAdc(spi,3)
        if n % 2 == 0:
            gx, gy, gz = sensor.read_data()
	#print datetime.now(), gx, gy, gz
	outfile.write("%s, %d, %d, %d \n" % (str(datetime.now()), gx, gy, gz))

checkgyro(gyrothreshold)

print "Gyro requirement satisfied"

starttime = datetime.now()
elaptime = (datetime.now() - starttime).total_seconds()

while elaptime < totalrecordtime:
    datawrite(outfile)
    print "Date record complete"
    time.sleep(3)
    elaptime = (datetime.now() - starttime).total_seconds()

outfile.close()

sys.exit()

os.system("sudo shutdown -h now")
