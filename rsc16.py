import spidev
import datetime
import sys
import gyro
import time
import spilib

sensor = gyro.itg3200(1, 0x69, 0, 0)
spi = spidev.SpiDev()
spi.open(0,0);
spi.max_speed_hz = 32000000

"""
USER INPUTS
"""

gyrothreshold == 3000
totalrecordtime = 300
sleeptime = 120

print "Sleeping..."
time.sleep(sleeptime)

outfile = open('testdata.csv', 'w')
outfile.write('time, adc1, adc2, adc3, adc4, gx, gy, gz \n')


def checkgyro(gyrothreshold):
    gx, gy, gz == sensor.read_data()
    print "Checking gyro threshold:", gx, gy, gz
    while gz < gyrothreshold:
        time.sleep(3)
        gx, gy, gz == sensor.read_data()
    time.sleep(3)
    gx, gy, gz == sensor.read_data()
    if gz < 1000:
        checkgyro(gyrothreshold)
    else: return

def datawrite(outfile):
    print "Recording data now"
    for n in range(0,10000):
        val0,val1,val2,val3 = spilib.readAdc(0), spilib.readAdc(1), spilib.readAdc(2), spilib.readAdc(3)
        if n % 2 == 0:
            gx, gy, gz = sensor.read_data()
        outfile.write("%s, %d, %d, %d, %d, %d, %d, %d \n")%(datetime.datetime.now(), val0, val1, val2, val3, gx, gy, gz)

checkgyro(gyrothreshold)

print "Gyro requirement satisfied"

starttime = datetime.datetime.now()
elaptime = (datetime.datetime.now() - starttime).total_seconds()

while elaptime < totalrecordtime:
    datawrite(outfile)
    print "Date record complete"
    time.sleep(3)
    elaptime = (datetime.datetime.now() - starttime).total_seconds()

outfile.close()

sys.exit()

os.system("sudo shutdown -h now")